import { useQuery, useMutation } from "@apollo/client";
import { GET_TASK_COMMENTS, ADD_COMMENT } from "../graphql/comments";

export default function TaskComments({ taskId }: { taskId: number }) {
    const { data } = useQuery(GET_TASK_COMMENTS, {
        variables: { taskId: Number(taskId) },
    });

    const [addComment] = useMutation(ADD_COMMENT, {
        refetchQueries: ["GetComments"],
    });

    const comments = data?.comments || [];

    return (
        <div className="mt-3 border-t pt-2">
            <p className="text-sm font-medium mb-1">Comments</p>

            {/* List comments */}
            {comments.length === 0 && (
                <p className="text-gray-400 text-sm">No comments yet</p>
            )}

            {comments.map((c: any) => (
                <p key={c.id} className="text-sm">
                    <span className="font-semibold">{c.authorEmail}:</span>{" "}
                    {c.content}
                </p>
            ))}

            {/* Add comment */}
            <form
                onSubmit={async (e) => {
                    e.preventDefault();
                    const form = e.target as HTMLFormElement;

                    const content = (form.elements.namedItem("content") as HTMLInputElement).value;
                    const email = (form.elements.namedItem("email") as HTMLInputElement).value;

                    await addComment({
                        variables: {
                            taskId: Number(taskId),
                            content,
                            authorEmail: email,
                        },
                    });

                    form.reset();
                }}
                className="mt-2 flex gap-2"
            >
                <input
                    name="content"
                    placeholder="Write comment..."
                    className="border p-1 rounded flex-1 text-sm"
                    required
                />

                <input
                    name="email"
                    placeholder="email"
                    className="border p-1 rounded text-sm"
                    required
                />

                <button
                    type="submit"
                    className="bg-gray-800 text-white text-sm px-2 py-1 rounded"
                >
                    Add
                </button>
            </form>
        </div>
    );
}
