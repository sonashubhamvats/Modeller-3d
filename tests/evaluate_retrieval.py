import argparse
import json
import logging
from collections import defaultdict
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAG_DATABASE = PROJECT_ROOT / "rag_database"
GOLDEN_SET = Path(__file__).with_name("retrieval_golden_set.json")
TOP_K = 3
MIN_HIT_AT_1 = 0.80
MIN_HIT_AT_K = 0.90
MIN_MRR = 0.85


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate Chroma retrieval against a golden set.")
    parser.add_argument(
        "--collection",
        default="landscape_prompts",
        choices=("landscape_prompts", "landscape_scripts"),
        help="Chroma collection to evaluate.",
    )
    parser.add_argument(
        "--golden-set",
        type=Path,
        default=GOLDEN_SET,
        help="Path to the JSON file containing queries and expected filenames.",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.WARNING)
    golden_set = args.golden_set.resolve()
    cases = json.loads(golden_set.read_text(encoding="utf-8"))
    client = chromadb.PersistentClient(path=str(RAG_DATABASE))

    try:
        collection = client.get_collection(args.collection)
    except chromadb.errors.NotFoundError as exc:
        raise RuntimeError(
            f"Collection {args.collection!r} is missing. Run `python -m backend.build_rag` "
            "from the project root before evaluating retrieval."
        ) from exc

    collection_size = collection.count()
    if collection_size == 0:
        raise RuntimeError(
            f"Collection {args.collection!r} is empty. Run `python -m backend.build_rag` "
            "from the project root before evaluating retrieval."
        )

    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    collection = client.get_collection(
        args.collection, embedding_function=embedding_function
    )
    k = min(TOP_K, collection_size)
    category_stats: dict[str, list[float]] = defaultdict(lambda: [0, 0, 0.0, 0])
    total_reciprocal_rank = 0.0
    hit_at_1 = 0
    hit_at_k = 0

    if not cases:
        raise RuntimeError(f"The golden set is empty: {golden_set}")
    print(
        f"Collection {args.collection}: {collection_size} documents; "
        f"evaluating {len(cases)} queries (top {k})."
    )
    for case in cases:
        result = collection.query(
            query_texts=[case["query"]],
            n_results=k,
            include=["metadatas", "distances"],
        )
        metadata = result["metadatas"][0]
        distances = result["distances"][0]
        ranked = [
            (item.get("filename", "<missing filename metadata>"), distance)
            for item, distance in zip(metadata, distances)
        ]
        expected = set(case["expected_filenames"])
        rank = next(
            (index for index, (filename, _) in enumerate(ranked, start=1) if filename in expected),
            None,
        )
        first_hit = rank == 1
        hit = rank is not None
        reciprocal_rank = 1 / rank if rank else 0.0

        hit_at_1 += int(first_hit)
        hit_at_k += int(hit)
        total_reciprocal_rank += reciprocal_rank
        stats = category_stats[case["category"]]
        stats[0] += int(first_hit)
        stats[1] += int(hit)
        stats[2] += reciprocal_rank
        stats[3] += 1

        print(f"\n[{case['category']}] {case['query']}")
        print(f"  expected: {', '.join(sorted(expected))}")
        for index, (filename, distance) in enumerate(ranked, start=1):
            marker = "  <-- expected" if filename in expected else ""
            print(f"  {index}. {filename} (distance={distance:.4f}){marker}")
        print(f"  reciprocal rank: {reciprocal_rank:.3f}")

    query_count = len(cases)
    hit1_score = hit_at_1 / query_count
    hitk_score = hit_at_k / query_count
    mrr_score = total_reciprocal_rank / query_count

    print("\nOverall retrieval metrics")
    print(f"  Hit@1: {hit_at_1}/{query_count} = {hit1_score:.1%}")
    print(f"  Hit@{k}: {hit_at_k}/{query_count} = {hitk_score:.1%}")
    print(f"  MRR: {mrr_score:.3f}")
    print("\nBy category")
    for category, stats in sorted(category_stats.items()):
        first, top_k_hits, reciprocal_sum, count = stats
        print(
            f"  {category}: Hit@1={first / count:.1%}, "
            f"Hit@{k}={top_k_hits / count:.1%}, "
            f"MRR={reciprocal_sum / count:.3f} ({count} queries)"
        )

    eligible = (
        hit1_score >= MIN_HIT_AT_1
        and hitk_score >= MIN_HIT_AT_K
        and mrr_score >= MIN_MRR
    )
    print(
        "\nDemo retrieval gate: "
        f"Hit@1 >= {MIN_HIT_AT_1:.0%}, "
        f"Hit@{k} >= {MIN_HIT_AT_K:.0%}, "
        f"MRR >= {MIN_MRR:.2f}"
    )
    print(f"Result: {'PASS' if eligible else 'NOT YET ELIGIBLE'}")
    return 0 if eligible else 1


if __name__ == "__main__":
    raise SystemExit(main())
