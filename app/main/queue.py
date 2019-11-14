import re

from app.models import Queue


class QueueControl:
    @staticmethod
    def get_queue():
        queue = sorted(Queue.query.all())

        return [{
            'number': index + 1,
            'name_surname': queue_element.owner[0].name + ' ' + queue_element.owner[0].surname,
            'lab_number': queue_element.lab_number,
            'status': queue_element.status
        } for index, queue_element in enumerate(queue)]

    @staticmethod
    def change_status(current_user, new_status):
        if current_user.queues.count() == 0:
            raise Exception('You are not in something queue')

        edited_queue = current_user.queues.first()
        for queue_element in current_user.queues:
            if edited_queue.lab_number > queue_element.lab_number:
                edited_queue = queue_element

        if new_status == 'Ready':
            if edited_queue.status == 'Doing HW':
                edited_queue.status = 'Ready HW'
            if edited_queue.status == 'Doing task':
                edited_queue.status = 'Ready task'
        else:
            if edited_queue.status == 'Ready HW':
                edited_queue.status = 'Doing HW'
            if edited_queue.status == 'Ready task':
                edited_queue.status = 'Doing task'
        edited_queue.commit_to_db()

    @staticmethod
    def add_to_queue(current_user, lab_number):
        for queue_element in current_user.queues:
            if queue_element.lab_number == lab_number:
                raise Exception('You have been already registered')

        queue_element = Queue(
            lab_number=lab_number,
            status='Not shuffled',
            priority=0
        )
        queue_element.commit_to_db()
        queue_element.set_owner(current_user)

    @staticmethod
    def get_next():
        queue = Queue.query.all()
        queue = sorted(queue, key=lambda queue: (queue.lab_number, queue.priority))

        for queue_element in queue:
            if re.match('^Ready', queue_element.status):
                return queue_element.owner[0].username

    @staticmethod
    def start_queue():
        pass

    @staticmethod
    def terminate_queue():
        pass
