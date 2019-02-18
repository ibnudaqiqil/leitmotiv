import abc
import pathlib

import torch


class Model(abc.ABC):
    '''High-level definition of a leitmotiv model.

    A model is something that is able to describe some data given a finite set
    of parameters.  For example, a linear regressor will describe a dataset via
    a hyperplane in some N-dimensional space.  The :class:`Model` describes the
    interface that all models must adhere to, such as being able to
    export/import their internal state and being trained on a sample from a
    data set.
    '''
    @abc.abstractmethod
    def train(self, data):
        '''Train the model on some data set.

        The model will specify what exactly the data should be.  In general, it
        is expected to be a :class:`torch.Tensor` object since that's the
        math library being used internally.  A call to this method will cause
        the model to run one training iteration.  It is not idempotent, since
        training requires updating the model's internal state.

        Parameters
        ----------
        data : :class:`torch.Tensor` or :class:`numpy.ndarray`
            a multi-dimensional array containing the training data

        Returns
        -------
        float or dict
            the current training cost(s)
        '''

    @abc.abstractmethod
    def infer(self, data):
        '''Apply the trained model onto some data.

        The model is expected to know how to apply its own interference on some
        sample data.

        Parameters
        ----------
        data : :class:`torch.Tensor` or :class:`numpy.ndarray`
            a multi-dimensional array containing the data to be processed by
            the model
        '''

    @abc.abstractmethod
    def to_dict(self):
        '''Convert the model into a dictionary representation.

        This must be implemented by the subclass to describe how the model is
        converted into a Python dictionary.

        Returns
        -------
        dict
            the model's internal state
        '''

    @abc.abstractstaticmethod
    def from_dict(model_dict):
        '''Generate a model from its internal state dictionary.

        Parameters
        ----------
        model_dict : dict
            dictionary representation of the model's internal state

        Returns
        -------
        :class:`Model` instance
            an instance of the particular model
        '''

    def save(self, path):
        '''Save the model to a file on disk.

        Parameters
        ----------
        path : pathlib.Path
            path to where the model will be saved
        '''
        path = pathlib.Path(path)
        model_dict = self.to_dict()
        torch.save(model_dict, path)

    @classmethod
    def load(cls, path):
        '''Load the model from the given file.

        Parameters
        ----------
        path : pathlib.Path
            path to where the model is saved

        Returns
        -------
        :class:`Model` instance
            an instance of the particular model
        '''
        path = pathlib.Path(path)
        model_dict = torch.load(path, map_location='cpu')
        return cls.from_dict(model_dict)
