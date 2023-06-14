import os

import typer
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from property_oracle.llm import example_questions, llm
from vectore_store.chroma import vectordb

example_questions_joined = "\n* ".join(example_questions)
example_questions_joined = f"\n* {example_questions_joined}"


def app_intro():
    typer.echo(
        typer.style(
            (
                f"\n\nWelcome to Property Oracle! Ask me anything about Australian Property. "
                f"\n\nHere are some example questions you can ask:\n{example_questions_joined}"
                f"\n\nType 'exit' to exit or 'new' to clear the conversation history."
            ),
            fg=typer.colors.BRIGHT_YELLOW,
        )
    )


def main():
    app_intro()
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(
        llm, vectordb.as_retriever(), memory=memory
    )
    while True:
        question = typer.prompt(typer.style("\nYou", fg=typer.colors.BRIGHT_GREEN))

        if question.lower() == "exit":
            typer.echo(
                typer.style("Property Oracle: Goodbye!", fg=typer.colors.BRIGHT_YELLOW)
            )
            break
        elif question.lower() == "new":
            # flush memory, clear terminal
            typer.echo(
                typer.style(
                    "Property Oracle: Clearing chat history..",
                    fg=typer.colors.BRIGHT_YELLOW,
                )
            )
            memory.clear()
            os.system("clear")
            app_intro()
            continue  # restart the while loop

        result = qa({"question": question})
        typer.echo(
            typer.style(f"\nProperty Oracle:{result['answer']}",
            fg=typer.colors.BRIGHT_YELLOW,
            )
        )


if __name__ == "__main__":
    typer.run(main)
