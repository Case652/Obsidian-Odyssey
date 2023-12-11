import App from "./components/App";
import ErrorPage from "./components/ErrorPage";
import Home from "./components/Home";
import Signup from "./components/Signup";
const routes = [
    {
        path: "/",
        element: <App />,
        errorElement: <ErrorPage />,
        children: [
            {
                path: "/",
                element: <Home />
            },
            {
                path:"signup",
                element: <Signup />
            }
        ]
    }
]
export default routes;