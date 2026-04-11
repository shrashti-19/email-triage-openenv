class EasyGrader:
    def grade(self, env, *args, **kwargs) -> float:
        processed = getattr(env, "processed", [])
        count = len(processed)

        score = 0.2 + (count * 0.05)
        return max(0.01, min(0.99, score))


class MediumGrader:
    def grade(self, env, *args, **kwargs) -> float:
        processed = getattr(env, "processed", [])
        count = len(processed)

        score = 0.3 + (count * 0.05)
        return max(0.01, min(0.99, score))


class HardGrader:
    def grade(self, env, *args, **kwargs) -> float:
        processed = getattr(env, "processed", [])
        count = len(processed)

        score = 0.4 + (count * 0.05)
        return max(0.01, min(0.99, score))
