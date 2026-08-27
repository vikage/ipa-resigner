#!/usr/bin/python3

import argparse
import os
import resign
import common

def copy_framework(bundle, framework):
	common.execute_shell_command("cp -rf {} {}/Frameworks".format(framework, bundle))

def extract_framework_name(path):
    parts = path.split('/')
    for part in parts:
        if part.endswith('.framework'):
            return part[:-len('.framework')]

    return None

def install_framework(bundle, framework):
	framework_name = extract_framework_name(framework)
	binary_name = common.get_binary_name(bundle)
	print("[INFO] Installing {} to {}".format(framework_name, binary_name))
	common.execute_shell_command("optool install -c load -p @rpath/{}.framework/{} -t {}/{}".format(framework_name, framework_name, bundle, binary_name))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Code sign an iOS IPA")
    parser.add_argument("--ipa", required=True, help="Path to the IPA payload directory")
    parser.add_argument("--framework", required=True, help="Path to the framework")
    parser.add_argument("--profile", required=True, help="Provisioning profile name")
    parser.add_argument("--certificate", required=True, help="Certificate name")
    parser.add_argument("--bundle_id", "--bundle-id", "--bundle", required=False, help="New bundle ID", dest="bundle_id")

    args = parser.parse_args()

    working_dir = "tmp"
    common.execute_shell_command("rm -rf {}".format(working_dir))
    common.unzip_ipa(args.ipa, working_dir)

    bundle = common.find_app_bundle(working_dir)
    copy_framework(bundle, args.framework)
    install_framework(bundle, args.framework)

    resign.process_resign(working_dir, args.profile, args.certificate, args.bundle_id)
