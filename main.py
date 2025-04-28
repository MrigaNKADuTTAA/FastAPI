
from fastapi import FastAPI, HTTPException, Query
from app.scraper import fetch_trending_repositories
from app.analyzer import analyze_repositories, semantic_similarity_analysis
from app.cache import cache_get, cache_set

app = FastAPI()

@app.get("/analyze/github/trending/{language}")
async def analyze_github_trending(
    language: str,
    use_semantic_similarity: bool = Query(False, description="Include semantic similarity analysis")
):
    try:
        cached_data = cache_get(language)
        if cached_data:
            return cached_data

        repositories = fetch_trending_repositories(language)
        graph_data = analyze_repositories(repositories)

        if use_semantic_similarity:
            semantic_edges = semantic_similarity_analysis(repositories)
            graph_data["edges"].extend(semantic_edges)

        cache_set(language, graph_data)
        return graph_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
