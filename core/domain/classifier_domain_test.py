# coding: utf-8
#
# Copyright 2016 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, softwar
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for classifier domain objects."""


from core.domain import classifier_domain
from core.tests import test_utils
import utils


class ClassifierDataDomainTests(test_utils.GenericTestBase):
    """Test the classifier domain."""

    def test_to_dict(self):
        expected_classifier_dict = {
            'classifier_id': 'job_request_id1',
            'exp_id': 'exp_id1',
            'exp_version_when_created': 1,
            'state_name': 'a state name',
            'algorithm_id': "LDAStringClassifier",
            'classifier_data': {'alpha': 1.0},
            'data_schema_version': 1
        }
        observed_classifier = classifier_domain.ClassifierData(
            expected_classifier_dict['classifier_id'],
            expected_classifier_dict['exp_id'],
            expected_classifier_dict['exp_version_when_created'],
            expected_classifier_dict['state_name'],
            expected_classifier_dict['algorithm_id'],
            expected_classifier_dict['classifier_data'],
            expected_classifier_dict['data_schema_version'])
        self.assertDictEqual(expected_classifier_dict,
                             observed_classifier.to_dict())

    def test_validation(self):
        """Tests to verify validate method of classifier domain."""

        # Verify no errors are raised for correct data.
        classifier_data = {
            '_alpha': 0.1,
            '_beta': 0.001,
            '_prediction_threshold': 0.5,
            '_training_iterations': 25,
            '_prediction_iterations': 5,
            '_num_labels': 10,
            '_num_docs': 12,
            '_num_words': 20,
            '_label_to_id': {'text': 1},
            '_word_to_id': {'hello': 2},
            '_w_dp': [],
            '_b_dl': [],
            '_l_dp': [],
            '_c_dl': [],
            '_c_lw': [],
            '_c_l': []
        }
        classifier_dict = {
            'classifier_id': 'job_request_id1',
            'exp_id': 'exp_id1',
            'exp_version_when_created': 1,
            'state_name': 'a state name',
            'algorithm_id': "LDAStringClassifier",
            'classifier_data': classifier_data,
            'data_schema_version': 1
        }
        classifier = classifier_domain.ClassifierData(
            classifier_dict['classifier_id'],
            classifier_dict['exp_id'],
            classifier_dict['exp_version_when_created'],
            classifier_dict['state_name'],
            classifier_dict['algorithm_id'],
            classifier_dict['classifier_data'],
            classifier_dict['data_schema_version'])
        classifier.validate()

        # Verify validation error is raised when int is provided instead of
        # string.
        classifier_dict['classifier_id'] = 1
        classifier = classifier_domain.ClassifierData(
            classifier_dict['classifier_id'],
            classifier_dict['exp_id'],
            classifier_dict['exp_version_when_created'],
            classifier_dict['state_name'],
            classifier_dict['algorithm_id'],
            classifier_dict['classifier_data'],
            classifier_dict['data_schema_version'])
        with self.assertRaisesRegexp(utils.ValidationError, (
            'Expected id to be a string')):
            classifier.validate()

        # Verify validation error is raised when string is provided instead of
        # int.
        classifier_dict['classifier_id'] = 'job_request_id1'
        classifier_dict['exp_version_when_created'] = 'abc'
        classifier = classifier_domain.ClassifierData(
            classifier_dict['classifier_id'],
            classifier_dict['exp_id'],
            classifier_dict['exp_version_when_created'],
            classifier_dict['state_name'],
            classifier_dict['algorithm_id'],
            classifier_dict['classifier_data'],
            classifier_dict['data_schema_version'])
        with self.assertRaisesRegexp(utils.ValidationError, (
            'Expected exp_version_when_created to be an int')):
            classifier.validate()

        # Verify valdation error is raised when invalid state_name is provided.
        classifier_dict['exp_version_when_created'] = 1
        classifier_dict['state_name'] = 'A string #'
        classifier = classifier_domain.ClassifierData(
            classifier_dict['classifier_id'],
            classifier_dict['exp_id'],
            classifier_dict['exp_version_when_created'],
            classifier_dict['state_name'],
            classifier_dict['algorithm_id'],
            classifier_dict['classifier_data'],
            classifier_dict['data_schema_version'])
        with self.assertRaisesRegexp(utils.ValidationError, (
            'Invalid character # in the state name')):
            classifier.validate()

        # Verify validation error is raised when invalid algorithm_id is
        # provided.
        classifier_dict['state_name'] = 'a state name'
        classifier_dict['algorithm_id'] = 'abc'
        classifier = classifier_domain.ClassifierData(
            classifier_dict['classifier_id'],
            classifier_dict['exp_id'],
            classifier_dict['exp_version_when_created'],
            classifier_dict['state_name'],
            classifier_dict['algorithm_id'],
            classifier_dict['classifier_data'],
            classifier_dict['data_schema_version'])
        with self.assertRaisesRegexp(utils.ValidationError, (
            'Invalid algorithm id')):
            classifier.validate()

        # Verify validation error is raised when list is provided for dict.
        classifier_dict['algorithm_id'] = "LDAStringClassifier"
        classifier_dict['classifier_data'] = []
        classifier = classifier_domain.ClassifierData(
            classifier_dict['classifier_id'],
            classifier_dict['exp_id'],
            classifier_dict['exp_version_when_created'],
            classifier_dict['state_name'],
            classifier_dict['algorithm_id'],
            classifier_dict['classifier_data'],
            classifier_dict['data_schema_version'])
        with self.assertRaisesRegexp(utils.ValidationError, (
            'Expected classifier_data to be a dict')):
            classifier.validate()


class ClassifierTrainingJobDomainTests(test_utils.GenericTestBase):
    """Test the ClassifierTrainingJob domain."""

    def _get_training_job_from_dict(self, training_job_dict):
        training_job = classifier_domain.ClassifierTrainingJob(
            training_job_dict['job_id'],
            training_job_dict['algorithm_id'],
            training_job_dict['interaction_id'],
            training_job_dict['exp_id'],
            training_job_dict['exp_version'],
            training_job_dict['state_name'],
            training_job_dict['status'],
            training_job_dict['training_data'])

        return training_job

    def test_to_dict(self):
        expected_training_job_dict = {
            'job_id': 'exp_id1.SOME_RANDOM_STRING',
            'algorithm_id': 'LDAStringClassifier',
            'interaction_id': 'TextInput',
            'exp_id': 'exp_id1',
            'exp_version': 1,
            'state_name': 'a state name',
            'status': 'NEW',
            'training_data': [
                {
                    'answer_group_index': 1,
                    'answers': ['a1', 'a2']
                },
                {
                    'answer_group_index': 2,
                    'answers': ['a2', 'a3']
                }
            ]
        }
        observed_training_job = self._get_training_job_from_dict(
            expected_training_job_dict)
        self.assertDictEqual(expected_training_job_dict,
                             observed_training_job.to_dict())

    def test_validation(self):
        """Tests to verify validate method of ClassifierTrainingJob domain."""

        # Verify no errors are raised for correct data.
        training_data = [
            {
                'answer_group_index': 1,
                'answers': ['a1', 'a2']
            },
            {
                'answer_group_index': 2,
                'answers': ['a2', 'a3']
            }
        ]
        training_job_dict = {
            'job_id': 'exp_id1.SOME_RANDOM_STRING',
            'exp_id': 'exp_id1',
            'exp_version': 1,
            'state_name': 'some state',
            'algorithm_id': 'LDAStringClassifier',
            'interaction_id': 'TextInput',
            'training_data': training_data,
            'status': 'NEW'
        }
        training_job = self._get_training_job_from_dict(training_job_dict)
        training_job.validate()

        # Verify validation error is raised when int is provided for instance id
        # instead of string.
        training_job_dict['job_id'] = 1
        training_job = self._get_training_job_from_dict(training_job_dict)
        with self.assertRaisesRegexp(utils.ValidationError, (
            'Expected id to be a string')):
            training_job.validate()

        # Verify validation error is raised when string is provided for
        # exp_version instead of int.
        training_job_dict['job_id'] = 'exp_id1.SOME_RANDOM_STRING'
        training_job_dict['exp_version'] = 'abc'
        training_job = self._get_training_job_from_dict(training_job_dict)
        with self.assertRaisesRegexp(utils.ValidationError, (
            'Expected exp_version to be an int')):
            training_job.validate()

        # Verify validation error is raised when invalid state_name is provided.
        training_job_dict['exp_version'] = 1
        training_job_dict['state_name'] = 'A string #'
        training_job = self._get_training_job_from_dict(training_job_dict)
        with self.assertRaisesRegexp(utils.ValidationError, (
            'Invalid character # in the state name')):
            training_job.validate()

        # Verify validation error is raised when invalid algorithm_id is
        # provided.
        training_job_dict['state_name'] = 'a state name'
        training_job_dict['algorithm_id'] = 'abc'
        training_job = self._get_training_job_from_dict(training_job_dict)
        with self.assertRaisesRegexp(utils.ValidationError, (
            'Invalid algorithm id')):
            training_job.validate()

        # Verify validation error is raised when dict is provided for list.
        training_job_dict['algorithm_id'] = 'LDAStringClassifier'
        training_job_dict['training_data'] = {}
        training_job = self._get_training_job_from_dict(training_job_dict)
        with self.assertRaisesRegexp(utils.ValidationError, (
            'Expected training_data to be a list')):
            training_job.validate()


class ClassifierExplorationMappingDomainTests(test_utils.GenericTestBase):
    """Tests for the ClassifierExplorationMapping domain."""

    def _get_mapping_from_dict(self, mapping_dict):
        mapping = classifier_domain.ClassifierExplorationMapping(
            mapping_dict['exp_id'],
            mapping_dict['exp_version'],
            mapping_dict['state_name'],
            mapping_dict['classifier_id'])

        return mapping

    def test_to_dict(self):
        expected_mapping_dict = {
            'exp_id': 'exp_id1',
            'exp_version': 2,
            'state_name': u'網站有中',
            'classifier_id': 'classifier_id1'
        }
        observed_mapping = self._get_mapping_from_dict(
            expected_mapping_dict)
        self.assertDictEqual(expected_mapping_dict,
                             observed_mapping.to_dict())

    def test_validation(self):
        """Tests to verify validate method of ClassifierExplorationMapping
        domain."""

        # Verify no errors are raised for correct data.
        mapping_dict = {
            'exp_id': 'exp_id1',
            'exp_version': 2,
            'state_name': u'網站有中',
            'classifier_id': 'classifier_id1'
        }
        mapping = self._get_mapping_from_dict(mapping_dict)
        mapping.validate()

        # Verify validation error is raised when int is provided for exp_id
        # instead of string.
        mapping_dict['exp_id'] = 1
        mapping = self._get_mapping_from_dict(mapping_dict)
        with self.assertRaisesRegexp(utils.ValidationError, (
            'Expected exp_id to be a string')):
            mapping.validate()

        # Verify validation error is raised when string is provided for
        # exp_version instead of int.
        mapping_dict['exp_id'] = 'exp_id1'
        mapping_dict['exp_version'] = '1'
        mapping = self._get_mapping_from_dict(mapping_dict)
        with self.assertRaisesRegexp(utils.ValidationError, (
            'Expected exp_version to be an int')):
            mapping.validate()
