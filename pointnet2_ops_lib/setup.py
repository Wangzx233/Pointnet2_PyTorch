import os
import os.path as osp
import glob
from setuptools import find_packages, setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

# 获取当前目录路径
this_dir = osp.dirname(osp.abspath(__file__))

# 定义扩展源代码根目录
ext_src_root = osp.join("pointnet2_ops", "_ext-src")

# 收集所有源文件
ext_sources = (
    glob.glob(osp.join(ext_src_root, "src", "*.cpp")) +
    glob.glob(osp.join(ext_src_root, "src", "*.cu"))
)

# 收集所有头文件
ext_headers = glob.glob(osp.join(ext_src_root, "include", "*"))

# 依赖要求
requirements = ["torch>=1.4"]

# 更新CUDA架构设置，移除不支持的架构
os.environ["TORCH_CUDA_ARCH_LIST"] = "6.0;6.1;7.0;7.5;8.0;8.6"

# 创建版本文件如果不存在
version_file = osp.join("pointnet2_ops", "_version.py")
if not osp.exists(version_file):
    with open(version_file, 'w') as f:
        f.write('__version__ = "0.1.0"')

# 读取版本
exec(open(version_file).read())

setup(
    name="pointnet2_ops",
    version=__version__,
    author="Erik Wijmans",
    packages=find_packages(),
    install_requires=requirements,
    ext_modules=[
        CUDAExtension(
            name="pointnet2_ops._ext",
            sources=ext_sources,
            extra_compile_args={
                "cxx": ["-O3"],
                "nvcc": [
                    "-O3",
                    "-Xfatbin",
                    "-compress-all",
                    "--expt-relaxed-constexpr",
                    "-D__CUDA_NO_HALF_OPERATORS__",
                    "-D__CUDA_NO_HALF_CONVERSIONS__",
                    "-D__CUDA_NO_HALF2_OPERATORS__",
                ]
            },
            include_dirs=[osp.join(this_dir, ext_src_root, "include")],
        )
    ],
    cmdclass={"build_ext": BuildExtension},
    include_package_data=True,
)