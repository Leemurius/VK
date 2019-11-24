import random
import enum

from app.models import Queue, db


class Statuses(enum.Enum):
    PROCESSING_HW = 0
    PROCESSING_TASK = 1
    READY_TASK = 2
    READY_HW = 3
    DOING_TASK = 4
    DOING_HW = 5
    NOT_SHUFFLED = 6


class QueueControl:
    @staticmethod
    def start_queue():
        queue = QueueControl.get_queue()

        for index in range(len(queue)):
            temp_list_for_shuffle = []
            temp_list_head = []

            # Filling lists
            for index_element in range(len(queue[index])):
                if queue[index][index_element].status == Statuses.NOT_SHUFFLED.value:
                    queue[index][index_element].status = Statuses.READY_HW.value
                    temp_list_for_shuffle.append(queue[index][index_element])
                else:
                    temp_list_head.append(queue[index][index_element])

            # Delete from old queue
            del queue[index][:]

            # Shuffle
            random.shuffle(temp_list_for_shuffle)

            # Create new queue
            queue[index] = temp_list_head + temp_list_for_shuffle

            # Set new priority
            for index_element in range(len(queue[index])):
                QueueControl.set_new_priority_for_isolated_queue(queue[index])  # commit inside

    @staticmethod
    def update_queue():
        queue = QueueControl.get_queue()
        for index in range(len(queue)):
            queue[index] = QueueControl.sort_isolated_queue(queue[index])
            QueueControl.set_new_priority_for_isolated_queue(queue[index])  # commit inside

    @staticmethod
    def get_queue():
        queue = [[] for i in range(10)]
        for queue_element in Queue.query.all():
            queue[queue_element.lab_number].append(queue_element)

        for index in range(len(queue)):
            queue[index] = QueueControl.sort_isolated_queue(queue[index])

        return queue

    @staticmethod
    def get_queue_in_dict():
        queue = QueueControl.get_queue()
        for index in range(len(queue)):
            queue[index] = QueueControl.sort_isolated_queue(queue[index])

        result = []
        index = 0
        next_queue_element = QueueControl.get_next_queue_element()
        for isolated_queue in queue:
            for queue_element in isolated_queue:
                result.append({
                    'number': index + 1,
                    'name_surname': queue_element.owner[0].name + ' ' +
                                    queue_element.owner[0].surname,
                    'lab_number': queue_element.lab_number,
                    'status': Statuses(queue_element.status).name,
                    'is_next': queue_element == next_queue_element
                })
                index += 1
        return result

    @staticmethod
    def get_first_index_in_queue_for(current_user):
        QueueControl.validate(current_user)

        min_queue = float('Inf')
        result_queue_element = None
        for queue_element in current_user.queues:
            if queue_element.lab_number < min_queue:
                min_queue, result_queue_element = queue_element.lab_number, queue_element

        return result_queue_element

    @staticmethod
    def get_next_queue_element():
        queue = QueueControl.get_queue()

        for isolated_queue in queue:
            for queue_element in isolated_queue:
                if Statuses(queue_element.status) in (Statuses.PROCESSING_HW,
                                                      Statuses.PROCESSING_TASK):
                    return queue_element
                if Statuses(queue_element.status) in (Statuses.READY_TASK, Statuses.READY_HW):
                    return queue_element
        return None

    @staticmethod
    def get_next_user():
        next_element = QueueControl.get_next_queue_element()
        if next_element:
            return next_element.owner[0]
        else:
            return None

    @staticmethod
    def get_status(current_user):
        QueueControl.validate(current_user)
        status = QueueControl.get_first_index_in_queue_for(current_user).status
        return Statuses(status).name

    @staticmethod
    def set_new_priority_for_isolated_queue(isolated_queue):
        for index_element in range(len(isolated_queue)):
            isolated_queue[index_element].priority = index_element
        QueueControl.commit_to_db(isolated_queue)

    @staticmethod
    def set_finished(queue_element):
        db.session.delete(queue_element)
        db.session.commit()

    @staticmethod
    def change_status(current_user, new_status):
        QueueControl.validate(current_user)

        edited_queue = QueueControl.get_first_index_in_queue_for(current_user)

        if new_status == 'Ready':
            if edited_queue.status == Statuses.DOING_HW.value:
                edited_queue.status = Statuses.READY_HW.value
                edited_queue.priority = float('Inf')
                QueueControl.update_queue()
            if edited_queue.status == Statuses.DOING_TASK.value:
                edited_queue.status = Statuses.READY_TASK.value
                edited_queue.priority = float('Inf')
                QueueControl.update_queue()
        elif new_status == 'Not ready':
            if edited_queue.status == Statuses.READY_HW.value:
                edited_queue.status = Statuses.DOING_HW.value
            if edited_queue.status == Statuses.READY_TASK.value:
                edited_queue.status = Statuses.DOING_TASK.value
        elif new_status == 'Processing':
            if edited_queue.status == Statuses.READY_HW.value:
                edited_queue.status = Statuses.PROCESSING_HW.value
            if edited_queue.status == Statuses.READY_TASK.value:
                edited_queue.status = Statuses.PROCESSING_TASK.value
        elif new_status == 'Passed':
            if edited_queue.status == Statuses.PROCESSING_HW.value:
                edited_queue.status = Statuses.DOING_TASK.value
            if edited_queue.status == Statuses.PROCESSING_TASK.value:
                QueueControl.set_finished(edited_queue)
        elif new_status == 'Not passed':
            if edited_queue.status == Statuses.PROCESSING_HW.value:
                edited_queue.status = Statuses.DOING_HW.value
            if edited_queue.status == Statuses.PROCESSING_TASK.value:
                edited_queue.status = Statuses.DOING_TASK.value

        edited_queue.commit_to_db()

    @staticmethod
    def add_to_queue(current_user, lab_number):
        for queue_element in current_user.queues:
            if queue_element.lab_number == lab_number:
                raise Exception('You have been already registered')

        queue_element = Queue(
            lab_number=lab_number,
            status=Statuses.NOT_SHUFFLED.value,
            priority=float('Inf')
        )
        queue_element.commit_to_db()
        queue_element.set_owner(current_user)

    @staticmethod
    def validate(current_user):
        if current_user.queues.count() == 0:
            raise Exception('You are not in something queue')

    @staticmethod
    def sort_isolated_queue(queue):
        return sorted(queue, key=lambda element: (element.status, element.priority))

    @staticmethod
    def commit_to_db(queue):
        for isolated_queue in queue:
            if isinstance(isolated_queue, list):
                for queue_element in isolated_queue:
                    queue_element.commit_to_db()
            else:
                isolated_queue.commit_to_db()
