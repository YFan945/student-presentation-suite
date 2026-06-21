from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

import jsonschema
import yaml

from shared.slide_spec_validation import semantic_errors


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads(
    (ROOT / "references" / "slide-spec.schema.json").read_text(encoding="utf-8")
)
VALID_GROUP = yaml.safe_load(
    (ROOT / "examples" / "ai-learning-report.yaml").read_text(encoding="utf-8")
)


def validation_errors(data: dict) -> list[str]:
    validator = jsonschema.Draft202012Validator(SCHEMA)
    schema_messages = [
        error.message
        for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path))
    ]
    return schema_messages + [item["message"] for item in semantic_errors(data)]


class SlideSpecValidationTests(unittest.TestCase):
    def test_valid_group_spec(self) -> None:
        self.assertEqual([], validation_errors(VALID_GROUP))

    def test_valid_individual_spec(self) -> None:
        spec = deepcopy(VALID_GROUP)
        spec["meta"]["format"] = "individual"
        spec["meta"].pop("members")
        for slide in spec["slides"]:
            slide["owner"] = "Individual"
        self.assertEqual([], validation_errors(spec))

    def test_rejects_non_contiguous_slide_ids(self) -> None:
        spec = deepcopy(VALID_GROUP)
        spec["slides"][1]["id"] = 4
        self.assertTrue(
            any("contiguous" in message for message in validation_errors(spec))
        )

    def test_rejects_slide_count_and_duration_mismatch(self) -> None:
        spec = deepcopy(VALID_GROUP)
        spec["meta"]["slide_count"] = 9
        spec["meta"]["duration_min"] = 20
        messages = validation_errors(spec)
        self.assertTrue(any("slide_count" in message for message in messages))
        self.assertTrue(any("duration_min" in message for message in messages))

    def test_rejects_unknown_group_owner(self) -> None:
        spec = deepcopy(VALID_GROUP)
        spec["slides"][0]["owner"] = "C"
        self.assertTrue(
            any("not listed in meta.members" in message for message in validation_errors(spec))
        )

    def test_requires_source_deck_for_improvement_fields(self) -> None:
        spec = deepcopy(VALID_GROUP)
        spec["edit_intent"] = "review-fix"
        self.assertTrue(
            any("source_deck is required" in message for message in validation_errors(spec))
        )

    def test_rejects_unknown_field_and_bad_output_prefix(self) -> None:
        spec = deepcopy(VALID_GROUP)
        spec["meta"]["unknown_option"] = True
        spec["meta"]["output_prefix"] = "bad prefix!"
        messages = validation_errors(spec)
        self.assertTrue(any("Additional properties" in message for message in messages))
        self.assertTrue(any("does not match" in message for message in messages))

    def test_accepts_controlled_generation_fields(self) -> None:
        spec = deepcopy(VALID_GROUP)
        spec["meta"].update(
            {
                "scenario": "course-report",
                "audience": {
                    "primary": "teacher",
                    "knowledge_level": "intermediate",
                    "grading_focus": ["evidence"],
                    "explanation_depth": "balanced",
                },
                "workflow_mode": "guided",
                "quality_tier": "high-score",
            }
        )
        spec["generation_controls"] = {
            "max_words_per_slide": 45,
            "visual_text_ratio": "balanced",
            "speaker_notes": True,
            "memorable_lines": False,
            "qa_cards": True,
            "citation_style": "GB-T-7714",
        }
        spec["revision_contract"] = {
            "mode": "partial",
            "targets": [2],
            "instruction": "Only strengthen evidence on slide 2.",
            "preserve_untargeted_slides": True,
        }
        spec["slides"][1]["locked_fields"] = ["title", "layout"]
        spec["slides"][1]["evidence"] = [
            {
                "type": "survey",
                "claim": "Students use AI for early drafts",
                "source": "Class survey",
                "status": "user-provided",
            }
        ]
        self.assertEqual([], validation_errors(spec))

    def test_rejects_invalid_partial_revision_and_unverified_source_claim(self) -> None:
        spec = deepcopy(VALID_GROUP)
        spec["revision_contract"] = {
            "mode": "partial",
            "targets": [99],
            "instruction": "Rewrite one slide.",
            "preserve_untargeted_slides": False,
        }
        spec["slides"][0]["evidence"] = [
            {
                "type": "data",
                "claim": "Result improved",
                "status": "verified",
            }
        ]
        messages = validation_errors(spec)
        self.assertTrue(any("targets do not exist" in message for message in messages))
        self.assertTrue(any("preserve_untargeted_slides=true" in message for message in messages))
        self.assertTrue(any("verified evidence requires a source" in message for message in messages))


if __name__ == "__main__":
    unittest.main()
