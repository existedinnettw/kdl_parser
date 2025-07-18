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
        "test/*",
        "include/*",
    )

    def requirements(self):
        self.requires("orocos-kdl/[>=1.5.1 <2]", transitive_headers=True, transitive_libs=True)
        self.requires("tinyxml/[>=2.6.0 <3]", transitive_headers=True)
        self.requires("tinyxml2/[>=11.0.0 <13.0.0]", transitive_headers=True)
        self.requires("urdfdom/[>=3.1.1 <5.0.0]", transitive_headers=True)
        self.tool_requires("cmake/[>=3.12 <5]")
        self.test_requires("gtest/[>=1.11 <2.0]")

    def validate(self):
        check_min_cppstd(self, "14")

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()
        tc = CMakeToolchain(self)
        if(not self.options.shared):
            tc.preprocessor_definitions["KDL_PARSER_STATIC"] = ""
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        if can_run(self):
            cmake.test()
        cmake.install()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["kdl_parser"]
        if not self.options.shared:
            self.cpp_info.defines = ["KDL_PARSER_STATIC"]