#include <limits>
#include <vector>
#include <iostream>

using namespace std;

// If the condition is not true, report an error and halt.
#define EXPECT(condition, message)  \
    do                              \
    {                               \
        if (!(condition))           \
            expect_failed(message); \
    } while (0)

void expect_failed(const string &message);

/*** One node ***/

class ab_node
{
public:
    // Keys stored in this node and the corresponding children
    // The vectors are large enough to accomodate one extra entry
    // in overflowing nodes.

    // TODO: how does the default destructor actually work?
    //       Does destructing ab_node cause the destruction of parent as well?
    ab_node *parent;
    vector<ab_node *> children;
    vector<int> keys;

    // If this node contains the given key, return true and set i to key's position.
    // Otherwise return false and set i to the first key greater than the given one.
    bool find_branch(int key, int &i)
    {
        i = 0;
        while (i < keys.size() && keys[i] <= key)
        {
            if (keys[i] == key)
                return true;
            i++;
        }
        return false;
    }


    // Insert a new key at posision i and add a new child between keys i and i+1.
    void insert_branch(int i, int key, ab_node *child)
    {
        keys.insert(keys.begin() + i, key);
        children.insert(children.begin() + i + 1, child);
    }

    // An auxiliary function for displaying a sub-tree under this node.
    void show(int indent);
};

/*** Tree ***/

class ab_tree
{
public:
    int a;         // Minimum allowed number of children
    int b;         // Maximum allowed number of children
    ab_node *root; // Root node (even a tree with no keys has a root)
    int num_nodes; // We keep track of how many nodes the tree has

    // Create a new node and return a pointer to it.
    ab_node *new_node()
    {
        ab_node *n = new ab_node;

        n->keys.reserve(b);
        n->children.reserve(b + 1);
        num_nodes++;
        return n;
    }

    // Delete a given node, assuming that its children have been already unlinked.
    void delete_node(ab_node *n)
    {
        num_nodes--;
        delete n;
    }

    // Constructor: initialize an empty tree with just the root.
    ab_tree(int a, int b)
    {
        EXPECT(a >= 2 && b >= 2 * a - 1, "Invalid values of a,b");
        this->a = a;
        this->b = b;
        num_nodes = 0;
        // The root has no keys and one null child pointer.
        root = new_node();
        root->children.push_back(nullptr);
    }

    // An auxiliary function for deleting a subtree recursively.
    void delete_tree(ab_node *n)
    {
        for (int i = 0; i < n->children.size(); i++)
            if (n->children[i])
                delete_tree(n->children[i]);
        delete_node(n);
    }

    // Destructor: delete all nodes.
    ~ab_tree()
    {
        delete_tree(root);
        EXPECT(num_nodes == 0, "Memory leak detected: some nodes were not deleted");
    }

    // Find a key: returns true if it is present in the tree.
    bool find(int key)
    {
        ab_node *n = root;
        while (n)
        {
            int i;
            if (n->find_branch(key, i))
                return true;
            n = n->children[i];
        }
        return false;
    }

    // Display the tree on standard output in human-readable form.
    void show();

    // Check that the data structure satisfies all invariants.
    void audit();

    bool is_oversized(ab_node *n)
    {
        return n->children.size() > b;
    }

    // recursively split oversize nodes
    void split(ab_node *n)
    {
        while (n != nullptr  && is_oversized(n))
        {
            if (n == root)
            {
                ab_node *new_root = new_node();
                new_root->children.push_back(n);
                n->parent = new_root;
                root = new_root;
            }
            
            int mid = n->keys.size() / 2;
            ab_node *right = new_node();
            right->parent = n->parent;
            // split children pointers
            right->children.insert(right->children.begin(), n->children.begin() + mid + 1, n->children.end());

            // split keys 
            right->keys.insert(right->keys.begin(), n->keys.begin() + mid + 1, n->keys.end());

            // rewire parent pointers to the right
            for (const auto &child : right->children) {
                if(child != nullptr)
                    child->parent = right;
            }

            int i;
            n->parent->find_branch(n->keys[mid], i);
            n->parent->insert_branch(i, n->keys[mid], right);

            n->keys.resize(mid);
            n->children.resize(mid + 1);

            n = n->parent;
        }
    }

    // Insert: add key to the tree (unless it was already present).
    void insert(int key)
    {

        ab_node *n = root;
        while (1)
        {
            int i;
            if (n->find_branch(key, i))
                // tree already contains the key
                return;

            if (n->children[i] == nullptr)
            {
                // key is not in the tree, insert it here
                n->insert_branch(i, key, nullptr);
                break;
            }
            n = n->children[i];
        }

        if (is_oversized(n))
            split(n);
    }
};
