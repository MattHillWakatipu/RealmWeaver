from langchain.text_splitter import RecursiveCharacterTextSplitter

with open('world/background.txt', 'r') as file:
    background = file.read()
    print(background)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=20
    )

    docs = text_splitter.create_documents([background])

    for document in docs:
        print(f'This is a document \n{document.page_content}\n******\n\n')
