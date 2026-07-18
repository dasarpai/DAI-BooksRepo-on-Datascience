from pathlib import Path
from pypdf import PdfWriter
from PIL import Image
import argparse
import io
import os
import re

SUPPORTED_EXTENSIONS = {".pdf", ".png"}


def as_local_path(path):
    """Use Windows extended-length paths so files near the 260-char limit open."""
    resolved = str(Path(path).resolve())
    if os.name == "nt" and not resolved.startswith("\\\\?\\"):
        return "\\\\?\\" + resolved
    return resolved


def natural_sort_key(path):
    """Sort file2.pdf before file10.pdf."""
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", path.name)
    ]


def png_to_pdf_stream(png_path):
    """Convert a PNG image to an in-memory single-page PDF."""
    with Image.open(png_path) as image:
        if image.mode in ("RGBA", "P", "LA"):
            image = image.convert("RGB")
        pdf_stream = io.BytesIO()
        image.save(pdf_stream, format="PDF")
        pdf_stream.seek(0)
        return pdf_stream


def collect_document_files(folder):
    document_files = []
    for extension in SUPPORTED_EXTENSIONS:
        document_files.extend(folder.glob(f"*{extension}"))
    return document_files


def combine_pdfs(folder_path, sort_order="name"):
    folder = Path(folder_path).resolve()

    if not folder.is_dir():
        raise ValueError(f"Folder does not exist: {folder}")

    document_files = collect_document_files(folder)

    if not document_files:
        raise ValueError("No PDF or PNG files found in the folder.")

    if sort_order == "modified":
        document_files.sort(key=lambda file: file.stat().st_mtime)
    else:
        document_files.sort(key=natural_sort_key)

    # Example: D:\Books\Quantum -> D:\Books\Quantum.pdf
    output_file = folder.parent / f"{folder.name}.pdf"

    writer = PdfWriter()

    for document_file in document_files:
        local_path = as_local_path(document_file)
        if not os.path.exists(local_path):
            raise FileNotFoundError(
                f"File not readable (path length {len(local_path)}): {document_file.name}"
            )
        print(f"Adding: {document_file.name}")
        if document_file.suffix.lower() == ".png":
            writer.append(png_to_pdf_stream(local_path))
        else:
            writer.append(local_path)

    with open(as_local_path(output_file), "wb") as file:
        writer.write(file)

    writer.close()
    print(f"\nCombined PDF created: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Combine all PDF and PNG files in a folder."
    )
    parser.add_argument("folder", help="Folder containing PDF and PNG files")
    parser.add_argument(
        "--sort",
        choices=["name", "modified"],
        default="name",
        help="Sorting order; default is name",
    )

    args = parser.parse_args()
    combine_pdfs(args.folder, args.sort)
