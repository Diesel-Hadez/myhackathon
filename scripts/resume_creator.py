def resume_creator(profile):
    """
    Create a short user description from template

    Args:
        profile: A list containg user's name, list of expertise and list of work experience
    Returns:
        A string with the profile description
    """
    name, expertise, work_exp = profile
    expertise = ", ".join(expertise)
    work_exp = ", ".join(work_exp)
    template = "My name is {}. My expertise are in {}. My work experience include {}"
    return template.format(name,expertise,work_exp)
