#include <kdl_parser/kdl_parser.hpp>

int main()
{
    KDL::Tree tree;
    std::string xml_string = "<robot name=\"test_robot\"><link name=\"base_link\"/></robot>";
    if (!kdl_parser::treeFromString(xml_string, tree))
    {
        return 1; // Failed to parse the KDL tree from the string
    }
    return 0;
}