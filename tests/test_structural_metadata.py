from ingestion.structural_metadata import (
    extract_module_from_filename,
    enrich_document_structure,
)


def test_extract_module_from_filename():
    assert (
        extract_module_from_filename(
            "Modulo_11_parte_2.PDF"
        )
        == "Módulo 11"
    )


def test_extract_module_from_filename_module_1():
    assert (
        extract_module_from_filename(
            "Modulo_1_parte_1.pdf"
        )
        == "Módulo 1"
    )


def test_extract_module_from_filename_without_module():
    assert (
        extract_module_from_filename(
            "documento.pdf"
        )
        is None
    )


def test_enrich_document_structure():

    document = [
        {
            "page": 31,
            "text": (
                "APURAÇÃO DE DÉBITOS\n\n"
                ". Nacionalmente uniforme;\n"
                ". Resultante da soma das alíquotas"
            ),
        }
    ]

    result = enrich_document_structure(
        document,
        "Modulo_11_parte_2.PDF",
    )

    assert result[0]["module"] == "Módulo 11"

    assert (
        result[0]["section"]
        == "APURAÇÃO DE DÉBITOS"
    )