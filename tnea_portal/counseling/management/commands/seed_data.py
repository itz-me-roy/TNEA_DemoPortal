import random
from django.core.management.base import BaseCommand
from counseling.models import College, Branch, Cutoff

COLLEGES = [
    ("1001", "College of Engineering, Guindy", "Chennai", "Chennai", "UNIV_DEPT"),
    ("2003", "PSG College of Technology", "Coimbatore", "Coimbatore", "GOVT_AIDED"),
    ("1201", "Government College of Technology", "Coimbatore", "Coimbatore", "GOVT"),
    ("2617", "Thiagarajar College of Engineering", "Madurai", "Madurai", "GOVT_AIDED"),
    ("2716", "SSN College of Engineering", "Kalavakkam", "Chengalpattu", "SELF_FIN"),
    ("1401", "Government College of Engineering, Salem", "Salem", "Salem", "GOVT"),
    ("2731", "Sri Sivasubramaniya Nadar College", "Kalavakkam", "Chengalpattu", "SELF_FIN"),
    ("2626", "Coimbatore Institute of Technology", "Coimbatore", "Coimbatore", "GOVT_AIDED"),
    ("1108", "Anna University Regional Campus", "Tiruchirappalli", "Tiruchirappalli", "UNIV_DEPT"),
    ("2742", "Kumaraguru College of Technology", "Coimbatore", "Coimbatore", "SELF_FIN"),
]

BRANCHES = [
    ("CS", "Computer Science and Engineering"),
    ("IT", "Information Technology"),
    ("EC", "Electronics and Communication Engineering"),
    ("EEE", "Electrical and Electronics Engineering"),
    ("MECH", "Mechanical Engineering"),
    ("CIVIL", "Civil Engineering"),
]

COMMUNITIES = ["OC", "BC", "BCM", "MBC", "SC", "SCA", "ST"]

# Rough base cutoff offsets per community relative to OC, for realistic spread
COMMUNITY_OFFSET = {
    "OC": 0, "BC": -3, "BCM": -4, "MBC": -5, "SC": -12, "SCA": -15, "ST": -18,
}


class Command(BaseCommand):
    help = "Seed the database with sample TNEA-style colleges, branches, and cutoffs."

    def handle(self, *args, **options):
        random.seed(42)

        branch_objs = {}
        for code, name in BRANCHES:
            branch, _ = Branch.objects.get_or_create(code=code, name=name)
            branch_objs[code] = branch

        college_objs = []
        for code, name, place, district, ctype in COLLEGES:
            college, _ = College.objects.get_or_create(
                college_code=code,
                defaults=dict(name=name, place=place, district=district, college_type=ctype),
            )
            college_objs.append(college)

        created_count = 0
        for college in college_objs:
            # Better-known colleges get higher base cutoffs
            base = random.uniform(175, 199) if college.college_type in ("UNIV_DEPT", "GOVT") else random.uniform(150, 195)
            for branch_code, branch in branch_objs.items():
                branch_base = base - random.uniform(0, 15)
                for community in COMMUNITIES:
                    mark = max(60, branch_base + COMMUNITY_OFFSET[community] - random.uniform(0, 4))
                    _, created = Cutoff.objects.get_or_create(
                        college=college,
                        branch=branch,
                        community=community,
                        year=2025,
                        defaults={"cutoff_mark": round(mark, 2)},
                    )
                    if created:
                        created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(college_objs)} colleges, {len(branch_objs)} branches, {created_count} cutoff records."
        ))