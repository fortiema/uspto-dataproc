from celery import Celery

app = Celery('tasks', 
             broker='amqp://guest@localhost//',
             backend='redis://localhost')

@app.task
def process_id(all_the_data_parameters_needed_to_process_in_this_computer):
    #code that does stuff
    return result