import { gql, useQuery } from "@apollo/client";
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

export default function ProjectsPage() {
    const [slug, setSlug] = useState("avg");

    const { data, loading, error } = useQuery(GET_PROJECTS, {
        variables: { slug },
    });

    return (
        <div className="max-w-5xl mx-auto">
            <h1 className="text-2xl font-semibold mb-4">Projects</h1>

            <input
                value={slug}
                onChange={(e) => setSlug(e.target.value)}
                className="border p-2 rounded w-full mb-4"
                placeholder="Enter organization slug"
            />

            {loading && <p>Loading...</p>}
            {error && <p className="text-red-500">Failed to load projects</p>}

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
