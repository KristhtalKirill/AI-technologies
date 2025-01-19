#!/bin/sh
# Set environment settings during RUN command execution for image building
# Used in cmake configuration, install and post-install commands

export py3_ver_mm_wod=$(python3 -c "import sys; print(\"\".join(map(str, sys.version_info[:2])))")
export py3_ver_mm=$(python3 -c "import sys; print(\".\".join(map(str, sys.version_info[:2])))")
export py3_ver_mmm=$(python3 -c "import sys; print(\".\".join(map(str, sys.version_info[:3])))")
export py3_inc_dir=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")
export py3_lib_dir=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
export py3_np_inc_dirs=${py3_lib_dir}/numpy/core/include

py3_lib_path=/usr/lib/x86_64-linux-gnu/libpython${py3_ver_mmm}.so

# TODO
if [ "${py3_ver_mm_wod}" = "36" ];
then
  py3_lib_path=$(locate "/usr/lib/x86_64-linux-gnu/libpython${py3_ver_mm}*.so");
fi

export py3_lib_path

printf "Environment vars for OpenCV build:\n  python3 versions: %s %s %s\n" "${py3_ver_mm_wod}" "${py3_ver_mm}" "${py3_ver_mmm}"
printf "  python3 include dir: %s\n" "${py3_inc_dir}"
printf "  python3 packages path dir: %s\n" "${py3_lib_dir}"
printf "  python3 numpy include dir: %s\n" "${py3_np_inc_dirs}"
printf "  python3 lib path: %s\n" "${py3_lib_path}"