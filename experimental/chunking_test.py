from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter

with open('world/the_blade_itself.txt', 'r', encoding='utf8') as file:
    background = file.read()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024,
        chunk_overlap=20
    )

    texts = text_splitter.split_text(background)
    for text in texts:
        print(f'{text}\n******')
    print(len(texts))
