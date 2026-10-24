from patterns.structural.composite.pattern import File, Folder


def run() -> None:
    print("=== Composite: File System ===")
    src = Folder("src").add(File("main.py", 1200)).add(File("utils.py", 800))
    docs = Folder("docs").add(File("README.md", 2048)).add(Folder("images").add(File("logo.png", 5120)))
    project = Folder("project").add(src).add(docs).add(File("LICENSE", 1100))

    print("\n".join(project.render()))
    print(f"Total project size: {project.get_size()} B")
    print(f"docs only        : {docs.get_size()} B")


if __name__ == "__main__":
    run()
