from tools.pdf_parser import parse_pdf


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
    """
    Paper Reader Agent (Stage 2)
    ---------------------------
    Reads a research paper PDF and extracts raw text.

    Input:
        state["paper_path"] (optional)

    Output:
        state["paper_text"]
        state["intermediate_results"]["paper_reader"]
    """
    paper_path = state.get("paper_path")
    if paper_path:
        paper_text = parse_pdf(paper_path)
        summary = "PDF parsed successfully. Raw text extracted."
    else:
        paper_text = ""
        summary = (
            "No PDF provided",
            "Paper Reader Agent expects 'paper_path' in state. "
        )
    
    state["paper_text"] = paper_text
    state["intermediate_results"]["paper_reader"] = {
        "summary": summary,
        "text_length" : len(paper_text), 
    }
    
    
    return state