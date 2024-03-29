import json
from os.path import relpath
import argparse
from pathlib2 import Path
import azureml
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.authentication import ServicePrincipalAuthentication


def info(msg, char="#", width=75):
    print("")
    print(char * width)
    print(char + "   %0*s" % ((-1 * width) + 5, msg) + char)
    print(char * width)


def get_ws(tenant_id, service_principal_id,
           service_principal_password, subscription_id, resource_group, workspace):  # noqa: E501
    auth_args = {
        'tenant_id': tenant_id,
        'service_principal_id': service_principal_id,
        'service_principal_password': service_principal_password
    }

    ws_args = {
        'auth': ServicePrincipalAuthentication(**auth_args),
        'subscription_id': subscription_id,
        'resource_group': resource_group
    }
    ws = Workspace.get(workspace, **ws_args)
    return ws


def run(mdl_path, model_name, ws, tgs):
    print(ws.get_details())

    print('\nSaving model {} to {}'.format(mdl_path, model_name))

    # Model Path needs to be relative
    mdl_path = relpath(mdl_path, '.')

    Model.register(ws, model_name=model_name, model_path=mdl_path, tags=tgs)
    print('Done!')


if __name__ == "__main__":
    # argparse stuff for model path and model name
    parser = argparse.ArgumentParser(description='sanity check on model')
    parser.add_argument('-b', '--base_path',
                        help='directory to base folder', default='./')
    parser.add_argument(
        '-m', '--model', help='path to model file', default='./model/spam_classifier.pkl')
    parser.add_argument(
        '-cv', '--count_vectorizer', help='path to count vectorizer file', default='./model/count_vec.pkl')
    parser.add_argument('-mn', '--model_name',
                        help='AML Model name', default='spam_classifier')
    parser.add_argument('-cvn', '--cv_name',
                        help='Count Vectorizer file name', default='count_vec.pkl')
    parser.add_argument('-t', '--tenant_id', help='tenant_id')
    parser.add_argument('-s', '--service_principal_id',
                        help='service_principal_id')
    parser.add_argument('-p', '--service_principal_password',
                        help='service_principal_password')
    parser.add_argument('-u', '--subscription_id', help='subscription_id')
    parser.add_argument('-r', '--resource_group', help='resource_group')
    parser.add_argument('-w', '--workspace', help='workspace')
    args = parser.parse_args()

    print('Azure ML SDK Version: {}'.format(azureml.core.VERSION))
    args.model = 'model/' + args.model
    model_path = str(Path(args.base_path).resolve(
        strict=False).joinpath(args.model).resolve(strict=False))
    cv_path = str(Path(args.base_path).resolve(
        strict=False).joinpath(args.count_vectorizer).resolve(strict=False))
    params_path = str(Path(args.base_path).resolve(
        strict=False).joinpath('params.json').resolve(strict=False))
    wsrgs = {
        'tenant_id': args.tenant_id,
        'service_principal_id': args.service_principal_id,
        'service_principal_password': args.service_principal_password,
        'subscription_id': args.subscription_id,
        'resource_group': args.resource_group,
        'workspace': args.workspace
    }
    rgs_model = {
        'mdl_path': model_path,
        'model_name': args.model_name
    }

    rgs_cv = {
        'mdl_path': cv_path,
        'model_name': args.cv_name
    }

    # printing out args for posterity
    for i in wsrgs:
        if i == 'service_principal_password':
            print('{} => **********'.format(i))
        else:
            print('{} => {}'.format(i, wsrgs[i]))

    for i in rgs_model:
        print('{} => {}'.format(i, rgs_model[i]))

    with(open(str(params_path), 'r')) as f:
        tags = json.load(f)

    print('\n\nUsing the following tags:')
    for tag in tags:
        print('{} => {}'.format(tag, tags[tag]))

    rgs_model['tgs'] = tags

    workspc = get_ws(**wsrgs)
    rgs_model['ws'] = workspc
    run(**rgs_model)

    rgs_cv['ws'] = workspc
    run(**rgs_cv)


    # python register.py --model_path v --model_name c --tenant_id c
    # --service_principal_id v --service_principal_password v
    # --subscription_id v --resource_group x --workspace c
