from celery import group

from .incoming import incoming
from .filter_and_score_post import filter_and_score_post
from .associate_conversations import associate_conversations
from .echo import echo


def stream_chain(gen):
    for result in gen:
        task_chain(result)

def task_chain(result):
    main_chain = (incoming.s() |
                echo.s() |
                group([
                    filter_and_score_post.s(),
                    associate_conversations.s()
                ]))
    main_chain.delay(result)
