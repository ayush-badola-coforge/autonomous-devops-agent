class Metrics:

    # -------------------------
    # Retrieval Metrics
    # -------------------------

    @staticmethod
    def hit_rate(expected_docs, retrieved_docs):

        if not expected_docs:
            return int(len(retrieved_docs) == 0)

        return int(
            any(
                doc in retrieved_docs
                for doc in expected_docs
            )
        )

    @staticmethod
    def precision_at_k(
        expected_docs,
        retrieved_docs
    ):

        if not retrieved_docs:
            return 0.0

        relevant_found = len(
            set(expected_docs)
            & set(retrieved_docs)
        )

        return relevant_found / len(retrieved_docs)

    @staticmethod
    def recall_at_k(
        expected_docs,
        retrieved_docs
    ):

        if not expected_docs:
            return 0.0

        relevant_found = len(
            set(expected_docs)
            & set(retrieved_docs)
        )

        return relevant_found / len(expected_docs)

    @staticmethod
    def f1_score(
        precision,
        recall
    ):

        if precision + recall == 0:
            return 0.0

        return (
            2 * precision * recall
        ) / (precision + recall)

    @staticmethod
    def mrr(
        expected_docs,
        retrieved_docs
    ):

        for idx, doc in enumerate(retrieved_docs):

            if doc in expected_docs:
                return 1 / (idx + 1)

        return 0.0

    @staticmethod
    def out_of_scope_score(
        expected_docs,
        retrieved_docs
    ):

        if expected_docs:
            return None

        return int(len(retrieved_docs) == 0)

    @staticmethod
    def retrieval_score(
        precision,
        recall,
        mrr,
        hit_rate
    ):

        return (
            0.30 * precision +
            0.30 * recall +
            0.20 * mrr +
            0.20 * hit_rate
        )

    
    @staticmethod
    def extract_score(value):
        rating_map = {
            "poor": 0,
            "moderate": 4,
            "good": 7,
            "excellent": 10
        }
        if isinstance(value, dict):
            value = value.get("assessment", "Poor")
        
        return rating_map.get(str(value).strip().lower(),0)

    @staticmethod
    def llm_answer_score(
        correctness,
        completeness,
        relevance,
        faithfulness,
        hallucination
    ): 
        return (
            Metrics.extract_score(correctness) +
            Metrics.extract_score(completeness) +
            Metrics.extract_score(relevance) +
            Metrics.extract_score(faithfulness) +
            Metrics.extract_score(hallucination)
        ) / 50

    @staticmethod
    def rag_score(
        retrieval_score,
        answer_score
    ):

        return (
            0.4 * retrieval_score +
            0.6 * answer_score
        )