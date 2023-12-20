import App from "./components/App";
import ErrorPage from "./components/ErrorPage";
import Signup from "./components/Signup";
import Battle from "./components/Battle";
import CharacterSelection from "./components/CharacterSelection";
import Town from "./components/Town";
import Victory from "./components/Victory";
import Defeat from "./components/Defeat";
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
            },
            {
                path:"victory",
                element: <Victory />
            },
            {
                path:"defeat",
                element: <Defeat />
            }
        ]
    }
]
export default routes;