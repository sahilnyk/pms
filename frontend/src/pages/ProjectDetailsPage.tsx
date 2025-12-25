import { useParams, Link } from "react-router-dom";
import { useQuery, useMutation } from "@apollo/client";
import { GET_PROJECT_DETAILS } from "../graphql/project";
import { CREATE_TASK } from "../graphql/task";
import { UPDATE_TASK_STATUS } from "../graphql/taskStatus";
import TaskComments from "../components/TaskComments";

export default function ProjectDetailsPage() {
    const { id } = useParams();

    const { data, loading, error } = useQuery(GET_PROJECT_DETAILS, {
        variables: { projectId: Number(id) },
    });

    const [createTask] = useMutation(CREATE_TASK, {
        refetchQueries: ["ProjectDetails"],
    });

    const [updateTaskStatus] = useMutation(UPDATE_TASK_STATUS, {
        refetchQueries: ["ProjectDetails"],
    });

    if (loading) return <p className="text-center">Loading...</p>;
    if (error) return <p className="text-red-500 text-center">Failed to load</p>;

    const tasks = data?.tasks || [];
    const stats = data?.projectStats;

    return (
        <div className="max-w-5xl mx-auto space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-semibold">Project #{id}</h1>

                <Link to="/" className="text-blue-500 underline">
                    Back
                </Link>
            </div>

            {stats && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <div className="p-3 bg-white border rounded shadow-sm">
                        <p className="text-gray-500 text-sm">Total</p>
                        <p className="text-xl font-bold">{stats.totalTasks}</p>
                    </div>

                    <div className="p-3 bg-white border rounded shadow-sm">
                        <p className="text-gray-500 text-sm">Completed</p>
                        <p className="text-xl font-bold">{stats.completedTasks}</p>
                    </div>

                    <div className="p-3 bg-white border rounded shadow-sm">
                        <p className="text-gray-500 text-sm">In Progress</p>
                        <p className="text-xl font-bold">{stats.inProgressTasks}</p>
                    </div>

                    <div className="p-3 bg-white border rounded shadow-sm">
                        <p className="text-gray-500 text-sm">Completion</p>
                        <p className="text-xl font-bold">{stats.completionRate}%</p>
                    </div>
                </div>
            )}

            <div>
                <h2 className="text-xl font-semibold mb-2">Tasks</h2>

                <form
                    onSubmit={async (e) => {
                        e.preventDefault();
                        const form = e.target as HTMLFormElement;

                        const title = (form.elements.namedItem("title") as HTMLInputElement).value;
                        const description = (form.elements.namedItem("description") as HTMLInputElement).value;

                        await createTask({
                            variables: {
                                projectId: Number(id),
                                title,
                                description,
                            },
                        });

                        form.reset();
                    }}
                    className="mb-4 space-y-2"
                >
                    <input
                        name="title"
                        placeholder="Task title"
                        className="border p-2 rounded w-full"
                        required
                    />

                    <input
                        name="description"
                        placeholder="Description"
                        className="border p-2 rounded w-full"
                    />

                    <button
                        type="submit"
                        className="bg-blue-500 text-white px-4 py-2 rounded"
                    >
                        Add Task
                    </button>
                </form>

                {tasks.length === 0 && (
                    <p className="text-gray-500">No tasks yet</p>
                )}

                <div className="space-y-3">
                    {tasks.map((task: any) => (
                        <div key={task.id} className="bg-white border rounded p-3 shadow-sm">
                            <div className="flex justify-between">
                                <p className="font-medium">{task.title}</p>

                                <select
                                    value={task.status}
                                    onChange={(e) =>
                                        updateTaskStatus({
                                            variables: {
                                                taskId: Number(task.id),
                                                status: e.target.value,
                                            },
                                        })
                                    }
                                    className="border px-2 py-1 rounded text-sm"
                                >
                                    <option value="TODO">TODO</option>
                                    <option value="IN_PROGRESS">IN_PROGRESS</option>
                                    <option value="DONE">DONE</option>
                                </select>
                            </div>

                            <p className="text-gray-500 text-sm">
                                {task.description || "No description"}
                            </p>

                            <p className="text-xs text-gray-400 mt-1">
                                Assigned: {task.assigneeEmail || "Unassigned"}
                            </p>

                            <TaskComments taskId={task.id} />
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
