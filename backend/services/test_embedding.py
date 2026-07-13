from backend.services.embedding_service import embedding_service


def main():

    text = "Segmentation Fault"

    embedding = embedding_service.generate_embedding(text)

    print(f"Embedding Length : {len(embedding)}")


if __name__ == "__main__":
    main()