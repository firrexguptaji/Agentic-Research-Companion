from tools.pdf_parser import parse_pdf_with_sections
from tools.vector_store import PaperVectorStore
from tools.text_chunker import chunk_text

def paper_reader_agent(state: dict) -> dict:
    # """
    # Paper Reader Agent(Stage 1)
    # ----------------------
    # Stimulates reading and understanding research papers.
    
    # Stage 1 behaviors:
    # - No PDF parsing
    # - No vector retrieval
    # - Returns placeholder understanding
    
    
    # Inputs: 
    #     - state: shared LangGraph state
    # Outputs:
    #     Updated state with paper Context
    # """
    
    # query = state.get("query","")
    
    # paper_summary = (
    #     "Paper Reader Agent: "
    #     "This agent would parse the research paper, "
    #     "identify section (abstract, method, results), "
    #     "and extract relevant context based on the query. "
    # )
    
    # state["intermediate_results"]["paper_reader"] = {
    #     "query" : query,
    #     "summary" : paper_summary
    # }
    # 
    """
    Paper Reader Agent (Stage 2.1)
    -----------------------------
    Parses a PDF into section-aware text blocks.
    """
    paper_path = state.get("paper_path")

    vector_store = PaperVectorStore()

    try:
        if paper_path:
            sections = parse_pdf_with_sections(paper_path)

            for section, text in sections.items():
                chunks = chunk_text(text)
                metadatas = [
                    {"section": section, "source": paper_path}
                    for _ in chunks
                ]

                vector_store.add_documents(chunks, metadatas)

            summary = "PDF parsed and indexed into vector store."
            paper_text = "\n\n".join(sections.values())
        else:
            sections = {}
            paper_text = ""
            summary = "No PDF provided."

    except Exception as e:
        sections = {}
        paper_text = ""
        summary = f"PDF parsing failed: {str(e)}"

    state["paper_text"] = paper_text
    state["paper_sections"] = sections
    state["vector_store"] = vector_store

    state["intermediate_results"]["paper_reader"] = {
        "summary": summary,
        "sections_found": list(sections.keys()),
        "text_length": len(paper_text),
    }

    return state