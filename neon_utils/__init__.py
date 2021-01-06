# NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
#
# Copyright 2008-2020 Neongecko.com Inc. | All Rights Reserved
#
# Notice of License - Duplicating this Notice of License near the start of any file containing
# a derivative of this software is a condition of license for this software.
# Friendly Licensing:
# No charge, open source royalty free use of the Neon AI software source and object is offered for
# educational users, noncommercial enthusiasts, Public Benefit Corporations (and LLCs) and
# Social Purpose Corporations (and LLCs). Developers can contact developers@neon.ai
# For commercial licensing, distribution of derivative works or redistribution please contact licenses@neon.ai
# Distributed on an "AS IS” basis without warranties or conditions of any kind, either express or implied.
# Trademarks of Neongecko: Neon AI(TM), Neon Assist (TM), Neon Communicator(TM), Klat(TM)
# Authors: Guy Daniels, Daniel McKnight, Regina Bloomstine, Elon Gasper, Richard Leeds
#
# Specialized conversational reconveyance options from Conversation Processing Intelligence Corp.
# US Patents 2008-2020: US7424516, US20140161250, US20140177813, US8638908, US8068604, US8553852, US10530923, US10530924
# China Patent: CN102017585  -  Europe Patent: EU2156652  -  Patents Pending

from neon_utils.skill_override_functions import *
from neon_utils.logger import LOG

SKILL = None
TYPE = None


def skill_needs_patching(skill):
    """
    Determines if the passed skill is running under a non-Neon core and needs to be patched for compatibility
    :param skill: MycroftSkill object to test
    :return: True if skill needs to be patched
    """
    return not hasattr(skill, "server")


def stub_missing_parameters(skill):
    global SKILL
    global TYPE

    SKILL = skill
    TYPE = type(skill)
    LOG.debug(SKILL)
    LOG.debug(TYPE)

    skill.server = False
    skill.gui_enabled = False  # TODO: Actually check for this somehow? DM

    # TODO: Iterate over functions instead of individual DM
    skill.neon_in_request = neon_in_request
    skill.neon_must_respond = neon_must_respond
    skill.speak_dialog = speak_dialog
    skill.speak = speak
