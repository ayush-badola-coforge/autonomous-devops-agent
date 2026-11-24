import json

from backend.rag_engine.rag_service import rag_service
from backend.evaluation.judge_llm import JudgeLLM
from backend.evaluation.metrics import Metrics


def run_evaluation():
    print("-1")
    with open(
        "backend/evaluation/ground_truth.json",
        "r",
        encoding="utf-8"
    ) as file:

        test_cases = json.load(file)

    print("-2")

    judge = JudgeLLM()

    results = []
    print("-3")
    for test_case in test_cases:
        print("-4")
        question = test_case["question"]
        print("-5")
        expected_docs = test_case.get(
            "expected_docs",
            []
        )
        print("-6")
        reference_answer = test_case.get(
            "reference_answer",
            ""
        )
        print("-7")

        # ----------------------------------
        # Generate RAG Answer
        # ----------------------------------

        try:

            result = rag_service.answer_with_context(
                question
            )
            print("1")

        except Exception as e:

            print(
                f"\nFAILED QUESTION: {question}"
            )

            print(
                f"ERROR: {str(e)}"
            )

            break

        print("2")

        generated_answer = result["answer"]
        print("3")
        retrieved_context = "\n".join(
            result["contexts"]
        )

        retrieved_docs = list(
            dict.fromkeys(
                result["sources"]
            )
        )

        # ----------------------------------
        # Retrieval Metrics
        # ----------------------------------

        hit_rate = Metrics.hit_rate(
            expected_docs,
            retrieved_docs
        )

        precision = Metrics.precision_at_k(
            expected_docs,
            retrieved_docs
        )

        recall = Metrics.recall_at_k(
            expected_docs,
            retrieved_docs
        )

        f1 = Metrics.f1_score(
            precision,
            recall
        )

        mrr = Metrics.mrr(
            expected_docs,
            retrieved_docs
        )

        retrieval_score = (
            Metrics.retrieval_score(
                precision,
                recall,
                mrr,
                hit_rate
            )
        )

        out_of_scope_score = (
            Metrics.out_of_scope_score(
                expected_docs,
                retrieved_docs
            )
        )

        # ----------------------------------
        # Judge Evaluation
        # ----------------------------------
        print("4")
        judge_scores = judge.evaluate(
            question=question,
            reference_answer=reference_answer,
            generated_answer=generated_answer
        )

        print("5")

        answer_score = Metrics.llm_answer_score(
            correctness=judge_scores["correctness"],
            completeness=judge_scores["completeness"],
            relevance=judge_scores["relevance"],
            faithfulness=judge_scores["faithfulness"],
            hallucination=judge_scores["hallucination"]
        )
        print("6")
        rag_score = Metrics.rag_score(
            retrieval_score,
            answer_score
        )

        # ----------------------------------
        # Result Row
        # ----------------------------------

        row = {

            "question": question,

            "category": test_case.get(
                "category",
                ""
            ),

            "expected_docs":
                expected_docs,

            "retrieved_docs":
                retrieved_docs,

            "generated_answer":
                generated_answer,

            "hit_rate":
                round(hit_rate, 4),

            "precision":
                round(precision, 4),

            "recall":
                round(recall, 4),

            "f1":
                round(f1, 4),

            "mrr":
                round(mrr, 4),

            "retrieval_score":
                round(
                    retrieval_score,
                    4
                ),

            "correctness":
                judge_scores["correctness"],

            "completeness":
                judge_scores["completeness"],

            "relevance":
                judge_scores["relevance"],

            "faithfulness":
                judge_scores["faithfulness"],

            "hallucination":
                judge_scores["hallucination"],

            "answer_score":
                round(
                    answer_score,
                    4
                ),

            "rag_score":
                round(
                    rag_score,
                    4
                )
        }

        if out_of_scope_score is not None:

            row[
                "out_of_scope_score"
            ] = out_of_scope_score

        results.append(row)

        # ----------------------------------
        # Console Output
        # ----------------------------------

        print("\n" + "=" * 70)

        print(
            f"Question: {question}"
        )

        print(
            f"Expected Docs: "
            f"{expected_docs}"
        )

        print(
            f"Retrieved Docs: "
            f"{retrieved_docs}"
        )

        print(
            f"Retrieval Score: "
            f"{retrieval_score:.4f}"
        )

        print(
            f"Answer Score: "
            f"{answer_score:.4f}"
        )

        print(
            f"RAG Score: "
            f"{rag_score:.4f}"
        )

    # ----------------------------------
    # Overall Metrics
    # ----------------------------------

    overall_metrics = {

        "avg_hit_rate":
            round(
                sum(
                    r["hit_rate"]
                    for r in results
                ) / len(results),
                4
            ),

        "avg_precision":
            round(
                sum(
                    r["precision"]
                    for r in results
                ) / len(results),
                4
            ),

        "avg_recall":
            round(
                sum(
                    r["recall"]
                    for r in results
                ) / len(results),
                4
            ),

        "avg_f1":
            round(
                sum(
                    r["f1"]
                    for r in results
                ) / len(results),
                4
            ),

        "avg_mrr":
            round(
                sum(
                    r["mrr"]
                    for r in results
                ) / len(results),
                4
            ),

        "avg_retrieval_score":
            round(
                sum(
                    r["retrieval_score"]
                    for r in results
                ) / len(results),
                4
            ),

        "avg_answer_score":
            round(
                sum(
                    r["answer_score"]
                    for r in results
                ) / len(results),
                4
            ),

        "avg_rag_score":
            round(
                sum(
                    r["rag_score"]
                    for r in results
                ) / len(results),
                4
            )
    }

    output = {

        "overall_metrics":
            overall_metrics,

        "results":
            results
    }

    with open(
        "backend/evaluation/evaluation_results.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=4
        )

    return output


if __name__ == "__main__":

    evaluation_results = (
        run_evaluation()
    )

    print("\n" + "=" * 70)
    print("FINAL RAG EVALUATION")
    print("=" * 70)

    print(
        json.dumps(
            evaluation_results[
                "overall_metrics"
            ],
            indent=4
        )
    )