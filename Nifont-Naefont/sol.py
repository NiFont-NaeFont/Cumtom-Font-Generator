import numpy
import pandas as pd
import os

import chainer
from chainer.functions import relu, dropout
from chainer import serializers

from chainer_chemistry.models.ggnn import GGNN
from chainer_chemistry.dataset.preprocessors.ggnn_preprocessor import GGNNPreprocessor
from chainer_chemistry.models.mlp import MLP
from chainer_chemistry.dataset.parsers import CSVFileParser
from chainer_chemistry.saliency.calculator.integrated_gradients_calculator import IntegratedGradientsCalculator
from chainer_chemistry.link_hooks.variable_monitor_link_hook import VariableMonitorLinkHook
from chainer_chemistry.saliency.visualizer.mol_visualizer import SmilesVisualizer
from chainer_chemistry.dataset.converters import concat_mols
from chainer_chemistry.saliency.visualizer.visualizer_utils import abs_max_scaler

# from first.forms import ConstructionForm
# from first.models import Construction

def postprocess_label(label_list):
    return numpy.asarray(label_list, dtype=numpy.float32)

# Read input data (smiles csv file)
preprocessor = GGNNPreprocessor()
parser = CSVFileParser(preprocessor, labels=None, smiles_col='SMILES', postprocess_label=postprocess_label)

# target: acetaminophen = CC(=O)NC1=CC=C(C=C1)O
input_path = 'C:\Users\82108\Desktop\중앙대학교\취준\해커톤\대웅\DaeWoong\Goodrug\\first\\temp.csv'

#Input 위치
target_smiles = "CC(=O)NC1=CC=C(C=C1)O"
pd.DataFrame({"SMILES": [target_smiles]}).to_csv(input_path, index=False)

inf_result = parser.parse(input_path, return_smiles=True)

# Model
def activation_relu_dropout(h):
    return dropout(relu(h), ratio=0.25)

class GraphConvPredictor(chainer.Chain):
    def __init__(self, graph_conv, mlp=None):
        super(GraphConvPredictor, self).__init__()
        with self.init_scope():
            self.graph_conv = graph_conv
            if isinstance(mlp, chainer.Link):
                self.mlp = mlp
        if not isinstance(mlp, chainer.Link):
            self.mlp = mlp

    def __call__(self, atoms, adjs):
        x = self.graph_conv(atoms, adjs)
        if self.mlp:
            x = self.mlp(x)
        return x

n_unit = 32
conv_layers = 4
class_num = 1
device = -1  # -1 for CPU, 0 for GPU

ggnn = GGNN(out_dim=n_unit, hidden_dim=n_unit, n_layers=conv_layers)
mlp = MLP(out_dim=class_num, hidden_dim=n_unit, activation=activation_relu_dropout)

predictor_ast = GraphConvPredictor(ggnn, mlp)
# Load model
serializers.load_npz('my.model', predictor_ast)

# Preprocess input data
inf_train = inf_result['dataset']
inf_smiles = inf_result['smiles']

calculator = IntegratedGradientsCalculator(
predictor_ast, steps=5, eval_fun=None, target_extractor=VariableMonitorLinkHook(ggnn.embed, timing='post'),
device=device)

visualizer = SmilesVisualizer()

saliency_samples_vanilla = calculator.compute(inf_train, batchsize=1,  M=1, converter=concat_mols)
method = 'raw'
saliency_vanilla = calculator.aggregate(saliency_samples_vanilla, ch_axis=3, method=method)
i = 0

# Save result image file
os.makedirs('results', exist_ok=True)
visualizer.visualize(saliency_vanilla[i], inf_smiles[i], visualize_ratio=0.7, scaler=abs_max_scaler,
                     save_filepath='C:\Users\82108\Desktop\중앙대학교\취준\해커톤\대웅\DaeWoong\Goodrug\\first\\temp.png'.format(i))