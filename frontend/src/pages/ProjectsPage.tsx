import { gql, useQuery, useMutation } from "@apollo/client";
import { Link } from "react-router-dom";
import { useState } from "react";

const GET_PROJECTS = gql`
  query Projects($slug: String!) {
    projects(organizationSlug: $slug) {
      id
      name
      status
      description
    }
  }
`;

const CREATE_PROJECT = gql`
  mutation CreateProject(
    $organizationSlug: String!
    $name: String!
    $description: String
  ) {
    createProject(
      organizationSlug: $organizationSlug
      name: $name
      description: $description
    ) {
      project {
        id
        name
        description
        status
      }
    }
  }
`;

export default function ProjectsPage() {
    const [slug, setSlug] = useState("avg");

    const { data, loading, error } = useQuery(GET_PROJECTS, {
        variables: { slug },
        skip: !slug
    });

    const [projectName, setProjectName] = useState("");
    const [projectDesc, setProjectDesc] = useState("");

    const [createProject, { loading: creating }] = useMutation(CREATE_PROJECT, {
        refetchQueries: ["Projects"],
    });

    const handleCreateProject = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!slug || !projectName) return;

        await createProject({
            variables: {
                organizationSlug: slug,
                name: projectName,
                description: projectDesc,
            },
        });

        setProjectName("");
        setProjectDesc("");
    };

    return (
        <div className="max-w-5xl mx-auto space-y-6">
            <h1 className="text-2xl font-semibold">Projects</h1>


            <input
                value={slug}
                onChange={(e) => setSlug(e.target.value)}
                className="border p-2 rounded w-full"
                placeholder="Enter organization slug"
            />

            <form
                onSubmit={handleCreateProject}
                className="border p-4 rounded shadow-sm bg-white space-y-2"
            >
                <h3 className="font-semibold">Create Project</h3>

                <input
                    className="border p-2 w-full"
                    placeholder="Project name"
                    value={projectName}
                    onChange={(e) => setProjectName(e.target.value)}
                    required
                />

                <input
                    className="border p-2 w-full"
                    placeholder="Description"
                    value={projectDesc}
                    onChange={(e) => setProjectDesc(e.target.value)}
                />

                <button
                    disabled={creating}
                    className="bg-blue-600 text-white px-3 py-1 rounded disabled:opacity-60"
                >
                    {creating ? "Creating..." : "Create"}
                </button>
            </form>

            {loading && <p>Loading...</p>}
            {error && <p className="text-red-500">Failed to load projects</p>}

            {!loading && data?.projects?.length === 0 && (
                <p className="text-gray-500">No projects found</p>
            )}

            <div className="grid gap-3">
                {data?.projects?.map((p: any) => (
                    <Link
                        key={p.id}
                        to={`/project/${p.id}`}
                        className="bg-white border rounded p-4 shadow-sm hover:shadow-md transition"
                    >
                        <div className="flex justify-between">
                            <p className="font-medium">{p.name}</p>
                            <span className="text-sm px-2 py-1 rounded bg-gray-100">
                                {p.status}
                            </span>
                        </div>

                        <p className="text-sm text-gray-500 mt-1">
                            {p.description || "No description"}
                        </p>
                    </Link>
                ))}
            </div>
        </div>
    );
}
