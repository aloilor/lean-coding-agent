from pathlib import Path
import unittest

from scripts import setup_project


REPO_ROOT = Path(__file__).parents[2]


class SkillCatalogTest(unittest.TestCase):
    def test_catalog_labels_recommendations_without_selecting_any_skills(self) -> None:
        catalog = setup_project.skill_catalog(REPO_ROOT / "skills")
        by_name = {skill["name"]: skill for skill in catalog}

        self.assertIn("engineering-standards", by_name)
        self.assertEqual(
            {
                "label": "recommended",
                "reason": "Useful for most coding projects.",
            },
            by_name["engineering-standards"]["recommendation"],
        )
        self.assertEqual(
            {
                "label": "recommended",
                "reason": "Useful when the project has a test suite.",
            },
            setup_project.skill_recommendation("tdd"),
        )
        self.assertEqual(
            {
                "label": "contextual option",
                "reason": "Choose it when the project needs HTTP API design guidance.",
            },
            by_name["rest-api-design"]["recommendation"],
        )
        self.assertTrue(all(skill["selected"] is False for skill in catalog))


if __name__ == "__main__":
    unittest.main()
