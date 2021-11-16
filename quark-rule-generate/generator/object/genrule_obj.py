

from quark.core.struct.ruleobject import RuleObject


class GenRuleObject(RuleObject):
    __slots__ = ["check_item", "_json_obj", "_crime",
                 "_permission", "_api", "_score", "rule_filename"]

    def __init__(self, json_obj):
        """
        According to customized JSON rules, calculate the weighted score and assessing the stages of the crime.

        :param json_obj:
        """
        # the state of five stages
        self.check_item = [False, False, False, False, False, False]

        self._json_obj = json_obj
        self._crime = self._json_obj["crime"]
        self._permission = self._json_obj["permission"]
        self._api = self._json_obj["api"]
        self._score = self._json_obj["score"]
        self.rule_filename = None

    def __repr__(self):
        return f"<RuleObject-{self.rule_filename}>"

    @property
    def crime(self):
        """
        Description of given crime.

        :return: a string of the crime
        """
        return self._crime

    @property
    def permission(self):
        """
        Permission requested by the apk to practice the crime.

        :return: a list of given permissions
        """
        return self._permission

    @property
    def api(self):
        """
        Key native APIs that do the action and target in order.

        :return: a list recording the APIs class_name and method_name in order
        """
        return self._api

    @property
    def score(self):
        """
        The value used to calculate the weighted score

        :return: integer
        """
        return self._score

    def get_score(self, confidence):
        """
        According to the state of the five stages, we calculate the weighted score based on exponential growth.
        For example, we captured the third stage in five stages, then the weighted score would be (2^3-1) / 2^4.

        2^(confidence - 1)

        :param confidence:
        :return: floating point
        """
        if confidence == 0:
            return 0
        return (2 ** (confidence - 1) * self._score) / 2 ** 4
