import typer
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

from llm import llm
from vectore_store.chroma import vectordb


def main():
    typer.echo(
        typer.style(
            "\nProperty Oracle: Welcome to Property Oracle! Please ask me a question.",
            fg=typer.colors.BRIGHT_YELLOW,
        )
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(
        llm, vectordb.as_retriever(), memory=memory
    )
    while True:
        question = typer.prompt(typer.style("\nYou ", fg=typer.colors.BRIGHT_GREEN))
        result = qa({"question": question})
        typer.echo(
            typer.style(
                f"\nProperty Oracle:{result['answer']}", fg=typer.colors.BRIGHT_YELLOW
            )
        )


if __name__ == "__main__":
    typer.run(main)
