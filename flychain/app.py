from app.ui_generator import create_ui_with_feedback, create_ui_without_feedback
from app.feedback_handlers import chat
from agent.agent import create_agent
import click


@click.command()
@click.option('--model', '-m', default='text-davinci-003')
@click.option('--history/--no-history', default=True)
@click.option('--temperature', type=int, default=0)
@click.option('--task', type=str, default='text-generation')
@click.option('--huggingface-pipeline-kwargs', type=dict, default=None)
@click.option('--huggingface-model-kwargs', type=dict, default=None)
@click.option('--feedback', type=bool, default=True)
@click.option('--ui_theme', type=str, default='gstaff/xkcd')
# For more themes: https://huggingface.co/spaces/gradio/theme-gallery

def deploy(model, history, temperature, task, huggingface_pipeline_kwargs, huggingface_model_kwargs, feedback, ui_theme):
    
    agent = create_agent(
        model=model, 
        chat_history=history, 
        temperature=temperature, 
        task=task, 
        huggingface_pipeline_kwargs=huggingface_pipeline_kwargs, 
        huggingface_model_kwargs=huggingface_model_kwargs
    )

    def respond(msg, chat_history):
        bot_msg = agent.run(msg)
        chat_history.append((msg, bot_msg))
        chat['msg'] = msg
        chat['bot_msg'] = bot_msg
        return "", chat_history

    if feedback:
        ChatUI = create_ui_with_feedback(respond, ui_theme)
    else:
        ChatUI = create_ui_without_feedback(respond, ui_theme)

    ChatUI.launch()

if __name__ == '__main__':
    deploy()
    