import { Suspense, lazy, useEffect, useState } from 'react';
import { Route, Routes } from 'react-router-dom';

import SignIn from './pages/Authentication/SignIn';
import SignUp from './pages/Authentication/SignUp';
import Loader from './common/Loader';
import Subscription from './pages/Dashboard/Subscription';

const Translate = lazy(() => import('./pages/Translate'));
const Chart = lazy(() => import('./pages/Chart'));
const FormElements = lazy(() => import('./pages/Form/FormElements'));
const FormLayout = lazy(() => import('./pages/Form/FormLayout'));
const Profile = lazy(() => import('./pages/Profile'));
const Settings = lazy(() => import('./pages/Settings'));
const Tables = lazy(() => import('./pages/Tables'));
const SignDictionary = lazy(() => import('./pages/SignDictionary'));
const TranslationHistory = lazy(() => import('./pages/TranslationHistory'));
const Upload = lazy(() => import('./pages/SignVideo/Upload'));
const Record = lazy(() => import('./pages/SignVideo/Record'));
const DefaultLayout = lazy(() => import('./layout/DefaultLayout'));

function App() {
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    setTimeout(() => setLoading(false), 1000);
  }, []);

  return loading ? (
    <Loader />
  ) : (
    <>
      <Routes>
        <Route path="/auth/signin" element={<SignIn />} />
        <Route path="/auth/signup" element={<SignUp />} />
        <Route element={<DefaultLayout />}>
          <Route index element={<Subscription />} />
          <Route
            path="/translate"
            element={
              <Suspense fallback={<Loader />}>
                <Translate />
              </Suspense>
            }
          />
          <Route
            path="/signdictionary"
            element={
              <Suspense fallback={<Loader />}>
                <SignDictionary />
              </Suspense>
            }
          />
          <Route
            path="/translationhistory"
            element={
              <Suspense fallback={<Loader />}>
                <TranslationHistory />
              </Suspense>
            }
          />
          <Route
            path="/profile"
            element={
              <Suspense fallback={<Loader />}>
                <Profile />
              </Suspense>
            }
          />
          <Route
            path="/forms/form-elements"
            element={
              <Suspense fallback={<Loader />}>
                <FormElements />
              </Suspense>
            }
          />
          <Route
            path="/forms/form-layout"
            element={
              <Suspense fallback={<Loader />}>
                <FormLayout />
              </Suspense>
            }
          />
          <Route
            path="/tables"
            element={
              <Suspense fallback={<Loader />}>
                <Tables />
              </Suspense>
            }
          />
          <Route
            path="/settings"
            element={
              <Suspense fallback={<Loader />}>
                <Settings />
              </Suspense>
            }
          />
          <Route
            path="/chart"
            element={
              <Suspense fallback={<Loader />}>
                <Chart />
              </Suspense>
            }
          />
          <Route
            path="/signvideo/upload"
            element={
              <Suspense fallback={<Loader />}>
                <Upload />
              </Suspense>
            }
          />
          <Route
            path="/signvideo/record"
            element={
              <Suspense fallback={<Loader />}>
                <Record />
              </Suspense>
            }
          />
        </Route>
      </Routes>
    </>
  );
}

export default App;
