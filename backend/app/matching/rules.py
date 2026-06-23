from app.models.farm_profile import FarmProfile
from app.models.grant import FarmType, Grant
from app.schemas.match_result import RuleCheck


def check_region(grant: Grant, profile: FarmProfile) -> RuleCheck | None:
    eligible = grant.eligibility.eligible_regions
    if not eligible:
        return None
    if profile.region not in eligible:
        regions = ", ".join(r.value for r in eligible)
        return RuleCheck(
            rule_name="region",
            passed=False,
            category="hard",
            reason=f"This scheme is only available in: {regions}. Your farm is in {profile.region.value}.",
        )
    return RuleCheck(
        rule_name="region",
        passed=True,
        category="hard",
        reason=f"Your farm's region ({profile.region.value}) is eligible.",
    )


def check_farm_type(grant: Grant, profile: FarmProfile) -> RuleCheck | None:
    crit = grant.eligibility
    if profile.farm_type in crit.excluded_farm_types:
        return RuleCheck(
            rule_name="farm_type",
            passed=False,
            category="hard",
            reason=f"Farm type {profile.farm_type.value} is excluded from this scheme.",
        )
    eligible = crit.eligible_farm_types
    if not eligible or FarmType.ANY in eligible:
        return None
    if profile.farm_type not in eligible:
        types = ", ".join(t.value for t in eligible)
        return RuleCheck(
            rule_name="farm_type",
            passed=False,
            category="hard",
            reason=f"This scheme is only available to: {types}. Your farm type is {profile.farm_type.value}.",
        )
    return RuleCheck(
        rule_name="farm_type",
        passed=True,
        category="hard",
        reason=f"Your farm type ({profile.farm_type.value}) is eligible.",
    )


def check_land_size(grant: Grant, profile: FarmProfile) -> RuleCheck | None:
    crit = grant.eligibility
    if crit.min_land_size_ha is None and crit.max_land_size_ha is None:
        return None
    if crit.min_land_size_ha is not None and profile.size_hectares < crit.min_land_size_ha:
        return RuleCheck(
            rule_name="land_size",
            passed=False,
            category="hard",
            reason=(
                f"Requires at least {crit.min_land_size_ha} hectares; "
                f"your farm has {profile.size_hectares} hectares."
            ),
        )
    if crit.max_land_size_ha is not None and profile.size_hectares > crit.max_land_size_ha:
        return RuleCheck(
            rule_name="land_size",
            passed=False,
            category="hard",
            reason=(
                f"This scheme is for farms up to {crit.max_land_size_ha} hectares; "
                f"your farm has {profile.size_hectares} hectares."
            ),
        )
    return RuleCheck(
        rule_name="land_size",
        passed=True,
        category="hard",
        reason=f"Your farm size ({profile.size_hectares} ha) meets the requirement.",
    )


def check_required_activities(grant: Grant, profile: FarmProfile) -> RuleCheck | None:
    required = grant.eligibility.required_activities
    if not required:
        return None
    if not any(activity in profile.activities for activity in required):
        activities = ", ".join(a.value for a in required)
        return RuleCheck(
            rule_name="required_activities",
            passed=False,
            category="soft",
            reason=f"This scheme requires at least one of these activities: {activities}.",
        )
    return RuleCheck(
        rule_name="required_activities",
        passed=True,
        category="soft",
        reason="Your farm's activities match at least one required activity.",
    )


def check_sbi_registration(grant: Grant, profile: FarmProfile) -> RuleCheck | None:
    if not grant.eligibility.requires_sbi:
        return None
    if not profile.has_sbi:
        return RuleCheck(
            rule_name="sbi_registration",
            passed=False,
            category="soft",
            reason="This scheme requires registration with the Rural Payments Agency (an SBI). Register to become eligible.",
        )
    return RuleCheck(
        rule_name="sbi_registration",
        passed=True,
        category="soft",
        reason="Your farm is registered with the Rural Payments Agency (has an SBI).",
    )


def check_existing_elm_agreement(grant: Grant, profile: FarmProfile) -> RuleCheck | None:
    if not grant.eligibility.requires_no_existing_elm_agreement:
        return None
    if profile.has_existing_elm_agreement:
        return RuleCheck(
            rule_name="existing_elm_agreement",
            passed=False,
            category="soft",
            reason="This scheme requires no existing ELM revenue agreement; your farm already has one.",
        )
    return RuleCheck(
        rule_name="existing_elm_agreement",
        passed=True,
        category="soft",
        reason="Your farm has no existing ELM revenue agreement.",
    )


def check_environmentally_significant_site(grant: Grant, profile: FarmProfile) -> RuleCheck | None:
    if not grant.eligibility.requires_environmentally_significant_site:
        return None
    if not profile.has_environmentally_significant_features:
        return RuleCheck(
            rule_name="environmentally_significant_site",
            passed=False,
            category="soft",
            reason=(
                "This scheme requires an environmentally significant site (e.g. SSSI, woodland, "
                "historic feature, common land); none was indicated for your farm."
            ),
        )
    return RuleCheck(
        rule_name="environmentally_significant_site",
        passed=True,
        category="soft",
        reason="Your farm has environmentally significant features.",
    )


def check_sfi_window_eligibility(grant: Grant, profile: FarmProfile) -> RuleCheck | None:
    if grant.special_rule != "sfi_window_1_or_2":
        return None
    is_small_farm = profile.size_hectares <= 50
    no_elm_agreement = not profile.has_existing_elm_agreement
    if is_small_farm or no_elm_agreement:
        window = "Window 1 (small farms or no existing ELM agreement)"
        return RuleCheck(
            rule_name="sfi_window",
            passed=True,
            category="soft",
            reason=f"Your farm qualifies for {window}.",
        )
    return RuleCheck(
        rule_name="sfi_window",
        passed=True,
        category="soft",
        reason="Your farm will need to apply in Window 2 (all eligible farms), opening September 2026.",
    )


RULES = [
    check_region,
    check_farm_type,
    check_land_size,
    check_required_activities,
    check_sbi_registration,
    check_existing_elm_agreement,
    check_environmentally_significant_site,
    check_sfi_window_eligibility,
]
