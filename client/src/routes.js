import App from "./components/App";
import ErrorPage from "./components/ErrorPage";
import Home from "./components/Home";
import Signup from "./components/Signup";
import Battle from "./components/Battle";
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
            },
            {
                path:"battle",
                element: <Battle />
            }
        ]
    }
]
export default routes;