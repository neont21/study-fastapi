from fastapi import APIRouter, BackgroundTasks

router = APIRouter(
    prefix='/send-notification',
    tags=['notify'])

def write_notification(email: str, message=''):
    with open('log.txt', mode='w') as email_file:
        content = f'notification for {email}: {message}'
        email_file.write(content)

@router.post('/{email}', tags=['notify'])
async def send_notification(email: str, bg_tasks: BackgroundTasks):
    bg_tasks.add_task(write_notification, email,
                      message='some notification')
    return {'message': 'Notification sent in the background'}
