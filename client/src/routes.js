import App from "./components/App";
import ErrorPage from "./components/ErrorPage";
import Signup from "./components/Signup";
import Battle from "./components/Battle";
import CharacterSelection from "./components/CharacterSelection";
import Town from "./components/Town";
const routes = [
    {
        path: "/",
        element: <App />,
        errorElement: <ErrorPage />,
        children: [
            {
                path: "/",
                element: <CharacterSelection />
            },
            {
                path:"signup",
                element: <Signup />
            },
            {
                path:"battle",
                element: <Battle />
            },
            {
                path:"town",
                element: <Town />
            }
        ]
    }
]
export default routes;