from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.build import check_min_cppstd, can_run
from conan.errors import ConanInvalidConfiguration


class kdl_parserRecipe(ConanFile):
    name = "kdl_parser"
    version = "2.12.1"
    package_type = "library"

    license = ""
    author = "orocos ()"
    url = ""
    description = " kdl_parser and kdl_parser_py provide tools to construct a KDL tree from an XML robot representation in URDF."
    topics = ("KDL", "URDF", "parser")

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {"shared": False, "fPIC": True}

    exports_sources = (
        "CMakeLists.txt",
        "src/*",
        "tests/*",
        "include/*",
    )

    def requirements(self):
        self.requires("orocos-kdl/[>=1.5.1 <2]")
        self.requires("tinyxml/[>=2.6.0 <3]")
        self.requires("tinyxml2/[>=11.0.0 <13.0.0]")
        self.requires("urdfdom/[>=3.1.1 <5.0.0]")
        self.requires("urdfdom_headers/[>=1.1.1 <2]")
        self.tool_requires("cmake/[>=3.12 <5]")
        self.test_requires("gtest/[>=1.11]")

    def validate(self):
        check_min_cppstd(self, "14")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.settings.os == "Windows" and not self.options.shared:
            raise ConanInvalidConfiguration(
                "Static libraries are not supported on Windows. Please set option 'shared=True'."
            )
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["kdl_parser"]
