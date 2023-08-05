import { ChangeEvent, useState, useRef, useEffect, useCallback } from 'react';
import axios from 'axios';
import Breadcrumb from '../components/Breadcrumb';
import SwitcherThree from '../components/SwitcherThree';
import Webcam from 'react-webcam';
const videoConstraints = {
  width: 720,
  height: 360,
  facingMode: 'user',
};
const Translate = () => {
  const [selectedLanguage, setSelectedLanguage] = useState('english');
  const [selectedModel, setSelectedModel] = useState('gesture');
  const [processing, setProcessing] = useState(false); // New state for processing status
  const [predictedWord, setPredictedWord] = useState('');
  const [isCaptureEnable, setCaptureEnable] = useState<boolean>(false);
  const [countdown, setCountdown] = useState(3); // Countdown duration in seconds
  const webcamRef = useRef<Webcam>(null);
  const handleLanguageChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    setSelectedLanguage(event.target.value);
  };
  const handleModelChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedModel(event.target.value);
  };
  const addSpace = () => {
    setPredictedWord((prevWord) => prevWord + ' ');
  };

  const deleteWord = () => {
    setPredictedWord((prevWord) => {
      const words = prevWord.split(' ');
      words.pop(); // Remove the last word
      return words.join(' ');
    });
  };
  const startCountdown = () => {
    setProcessing(true); // Set processing to true before starting
    setCountdown(3); // Reset countdown value
    const countdownInterval = setInterval(() => {
      setCountdown((prevCountdown) => prevCountdown - 1);
    }, 1000); // Countdown every 1 second

    setTimeout(async () => {
      clearInterval(countdownInterval);
    }, countdown * 1000); // Wait for the countdown duration before starting action
  };
  const gesture = useCallback(async () => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      const response = await axios.post('http://localhost:5000/gesture', {
        language: selectedLanguage,
        image: imageSrc,
      });
      console.log(response.data);
      setPredictedWord((prevWord) => prevWord + response.data.sentence);
    }
    setProcessing(false); // Set processing to false to end
  }, [webcamRef]);
  const action = useCallback(async () => {
    setProcessing(true); // Set processing to true before starting
    startCountdown();
    const numberOfScreenshots = 30;
    const screenshots = [];
    for (let i = 0; i < numberOfScreenshots; i++) {
      const imageSrc = webcamRef.current?.getScreenshot();
      if (imageSrc) {
        screenshots.push(imageSrc);
        await new Promise((resolve) => setTimeout(resolve, 100)); // Delay between screenshots
      }
    }
    if (screenshots.length > 0) {
      try {
        const response = await axios.post('http://localhost:5000/action', {
          language: selectedLanguage,
          images: screenshots,
        });
        console.log(response.data);
        // Handle the response as needed
        setPredictedWord((prevWord) => prevWord + response.data.sentence);
      } catch (error) {
        console.error('Error sending batch:', error);
        // Handle the error appropriately
      }
    }
    setProcessing(false); // Set processing to false to end
  }, [webcamRef, selectedLanguage]);
  const handlePredictClick = async () => {
    if (selectedModel === 'gesture') {
      await gesture();
    } else if (selectedModel === 'action') {
      await action();
    }
  };
  return (
    <>
      <Breadcrumb pageName="Start Translation" />

      <div className="rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
        <div className="flex flex-col gap-5.5 p-6.5">
          <div className="mb-5.5 mt-10 flex flex-col gap-5.5 sm:flex-row">
            <div className="w-full sm:w-1/2">
              <div className="mb-4 flex items-center">
                <label className="mr-3 text-black dark:text-white">
                  Turn on Webcam:
                </label>
                <SwitcherThree
                  onChange={() => {
                    setCaptureEnable(!isCaptureEnable);
                  }}
                />
              </div>
            <div className='relative'>
              {isCaptureEnable && (
                <div className="camera-container">
                  <Webcam
                    audio={false}
                    width={540}
                    height={420}
                    ref={webcamRef}
                    screenshotFormat="image/jpeg"
                    videoConstraints={videoConstraints}
                  />
                </div>
              )}
            </div>
            {selectedModel === 'action' && countdown > 0 && (
            <div className="absolute flex justify-center items-center top-100 left-60">
            <span className="text-white text-4xl w-1/1 text-center">{countdown != 3 ? `Starting in ${countdown}` : ""}</span>
            </div> )}
            </div>

            <div className="w-full sm:w-1/2">
              <label className="mb-4 mt-1.5 block text-black dark:text-white">
                Sentence Predicted:
              </label>
              <textarea
                rows={14}
                placeholder="Translating the sentence.."
                className="w-full rounded-lg border-[1.5px] border-strokewhite bg-transparent py-3 px-5 font-medium text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:border-form-strokedark dark:bg-form-input dark:text-white dark:focus:border-primary"
                value={predictedWord}
                readOnly
              ></textarea>
              <div className="mt-4 flex gap-5">
                <button
                  className="inline-flex items-center justify-center rounded-md bg-meta-12 py-3  px-10 text-center font-medium text-white hover:bg-opacity-90 dark:bg-meta-3 lg:px-8 xl:px-7"
                  type="button"
                  onClick={addSpace}
                >
                  Space
                </button>
                <button
                  className="inline-flex items-center justify-center rounded-md bg-meta-11 py-3 px-10 text-center font-medium text-white hover:bg-opacity-90 dark:bg-meta-10 lg:px-8 xl:px-8"
                  type="button"
                  onClick={deleteWord}
                >
                  Delete Word
                </button>
              </div>
            </div>
          </div>

          <form>
            <div className="mb-5.5 mt-2 flex flex-col gap-5.5 sm:flex-row">
              <div className="w-full sm:w-1/4">
                <label className="mb-3 block text-black dark:text-white">
                  Select Language
                </label>
                <div className="relative z-20 bg-white dark:bg-form-input">
                  <span className="absolute top-1/2 left-4 z-30 -translate-y-1/2">
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 20 20"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <g opacity="0.8">
                        <path
                          fillRule="evenodd"
                          clipRule="evenodd"
                          d="M10.0007 2.50065C5.85852 2.50065 2.50065 5.85852 2.50065 10.0007C2.50065 14.1428 5.85852 17.5007 10.0007 17.5007C14.1428 17.5007 17.5007 14.1428 17.5007 10.0007C17.5007 5.85852 14.1428 2.50065 10.0007 2.50065ZM0.833984 10.0007C0.833984 4.93804 4.93804 0.833984 10.0007 0.833984C15.0633 0.833984 19.1673 4.93804 19.1673 10.0007C19.1673 15.0633 15.0633 19.1673 10.0007 19.1673C4.93804 19.1673 0.833984 15.0633 0.833984 10.0007Z"
                          fill="#637381"
                        ></path>
                        <path
                          fillRule="evenodd"
                          clipRule="evenodd"
                          d="M0.833984 9.99935C0.833984 9.53911 1.20708 9.16602 1.66732 9.16602H18.334C18.7942 9.16602 19.1673 9.53911 19.1673 9.99935C19.1673 10.4596 18.7942 10.8327 18.334 10.8327H1.66732C1.20708 10.8327 0.833984 10.4596 0.833984 9.99935Z"
                          fill="#637381"
                        ></path>
                        <path
                          fillRule="evenodd"
                          clipRule="evenodd"
                          d="M7.50084 10.0008C7.55796 12.5632 8.4392 15.0301 10.0006 17.0418C11.5621 15.0301 12.4433 12.5632 12.5005 10.0008C12.4433 7.43845 11.5621 4.97153 10.0007 2.95982C8.4392 4.97153 7.55796 7.43845 7.50084 10.0008ZM10.0007 1.66749L9.38536 1.10547C7.16473 3.53658 5.90275 6.69153 5.83417 9.98346C5.83392 9.99503 5.83392 10.0066 5.83417 10.0182C5.90275 13.3101 7.16473 16.4651 9.38536 18.8962C9.54325 19.069 9.76655 19.1675 10.0007 19.1675C10.2348 19.1675 10.4581 19.069 10.6159 18.8962C12.8366 16.4651 14.0986 13.3101 14.1671 10.0182C14.1674 10.0066 14.1674 9.99503 14.1671 9.98346C14.0986 6.69153 12.8366 3.53658 10.6159 1.10547L10.0007 1.66749Z"
                          fill="#637381"
                        ></path>
                      </g>
                    </svg>
                  </span>
                  <select
                    className="relative z-20 w-full appearance-none rounded border border-strokewhite bg-transparent py-3 px-12 outline-none transition focus:border-primary active:border-primary dark:border-form-strokedark dark:bg-form-input"
                    defaultValue={'english'}
                    onChange={handleLanguageChange}
                  >
                    <option value="english">English</option>
                    <option value="chinese">Chinese</option>
                    <option value="japanese">Japanese</option>
                  </select>
                  <span className="absolute top-1/2 right-4 z-10 -translate-y-1/2">
                    <svg
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <g opacity="0.8">
                        <path
                          fillRule="evenodd"
                          clipRule="evenodd"
                          d="M5.29289 8.29289C5.68342 7.90237 6.31658 7.90237 6.70711 8.29289L12 13.5858L17.2929 8.29289C17.6834 7.90237 18.3166 7.90237 18.7071 8.29289C19.0976 8.68342 19.0976 9.31658 18.7071 9.70711L12.7071 15.7071C12.3166 16.0976 11.6834 16.0976 11.2929 15.7071L5.29289 9.70711C4.90237 9.31658 4.90237 8.68342 5.29289 8.29289Z"
                          fill="#637381"
                        ></path>
                      </g>
                    </svg>
                  </span>
                </div>
              </div>

              <div className="w-full sm:w-1/4">
                <label className="mb-3 block text-black dark:text-white">
                  Select Model
                </label>
                <div className="relative z-20 bg-white dark:bg-form-input">
                  <span className="absolute top-1/2 left-4 z-30 -translate-y-1/2">
                    <svg
                      width="20"
                      height="20"
                      viewBox="0 0 20 20"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <g opacity="0.8">
                        <path
                          fillRule="evenodd"
                          clipRule="evenodd"
                          d="M10.0007 2.50065C5.85852 2.50065 2.50065 5.85852 2.50065 10.0007C2.50065 14.1428 5.85852 17.5007 10.0007 17.5007C14.1428 17.5007 17.5007 14.1428 17.5007 10.0007C17.5007 5.85852 14.1428 2.50065 10.0007 2.50065ZM0.833984 10.0007C0.833984 4.93804 4.93804 0.833984 10.0007 0.833984C15.0633 0.833984 19.1673 4.93804 19.1673 10.0007C19.1673 15.0633 15.0633 19.1673 10.0007 19.1673C4.93804 19.1673 0.833984 15.0633 0.833984 10.0007Z"
                          fill="#637381"
                        ></path>
                        <path
                          fillRule="evenodd"
                          clipRule="evenodd"
                          d="M0.833984 9.99935C0.833984 9.53911 1.20708 9.16602 1.66732 9.16602H18.334C18.7942 9.16602 19.1673 9.53911 19.1673 9.99935C19.1673 10.4596 18.7942 10.8327 18.334 10.8327H1.66732C1.20708 10.8327 0.833984 10.4596 0.833984 9.99935Z"
                          fill="#637381"
                        ></path>
                        <path
                          fillRule="evenodd"
                          clipRule="evenodd"
                          d="M7.50084 10.0008C7.55796 12.5632 8.4392 15.0301 10.0006 17.0418C11.5621 15.0301 12.4433 12.5632 12.5005 10.0008C12.4433 7.43845 11.5621 4.97153 10.0007 2.95982C8.4392 4.97153 7.55796 7.43845 7.50084 10.0008ZM10.0007 1.66749L9.38536 1.10547C7.16473 3.53658 5.90275 6.69153 5.83417 9.98346C5.83392 9.99503 5.83392 10.0066 5.83417 10.0182C5.90275 13.3101 7.16473 16.4651 9.38536 18.8962C9.54325 19.069 9.76655 19.1675 10.0007 19.1675C10.2348 19.1675 10.4581 19.069 10.6159 18.8962C12.8366 16.4651 14.0986 13.3101 14.1671 10.0182C14.1674 10.0066 14.1674 9.99503 14.1671 9.98346C14.0986 6.69153 12.8366 3.53658 10.6159 1.10547L10.0007 1.66749Z"
                          fill="#637381"
                        ></path>
                      </g>
                    </svg>
                  </span>
                  <select
                    className="relative z-20 w-full appearance-none rounded border border-strokewhite bg-transparent py-3 px-12 outline-none transition focus:border-primary active:border-primary dark:border-form-strokedark dark:bg-form-input"
                    defaultValue={'gesture'}
                    onChange={handleModelChange}
                  >
                    <option value="gesture">Gesture</option>
                    <option value="action">Action</option>
                  </select>
                  <span className="absolute top-1/2 right-4 z-10 -translate-y-1/2">
                    <svg
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <g opacity="0.8">
                        <path
                          fillRule="evenodd"
                          clipRule="evenodd"
                          d="M5.29289 8.29289C5.68342 7.90237 6.31658 7.90237 6.70711 8.29289L12 13.5858L17.2929 8.29289C17.6834 7.90237 18.3166 7.90237 18.7071 8.29289C19.0976 8.68342 19.0976 9.31658 18.7071 9.70711L12.7071 15.7071C12.3166 16.0976 11.6834 16.0976 11.2929 15.7071L5.29289 9.70711C4.90237 9.31658 4.90237 8.68342 5.29289 8.29289Z"
                          fill="#637381"
                        ></path>
                      </g>
                    </svg>
                  </span>
                </div>
              </div>

              <div className="flex w-full items-center justify-end sm:w-1/2">
                <div className="mt-8.5 flex gap-5">
                  <button
                    className="inline-flex items-center justify-center rounded bg-meta-13 py-3 px-10 text-center font-medium text-white hover:bg-opacity-90 dark:bg-primary lg:px-8 xl:px-7"
                    type="button"
                    onClick={handlePredictClick}
                    disabled={processing} // Disable the button when processing is true
                  >
                    {selectedModel === 'action' && countdown > 0
                      ? processing
                      ? `Starting in ${countdown}`
                      : 'Start Predict'
                      : processing
                      ? 'Processing...'
                      : 'Start Predict'}
                  </button>

                  <button
                    className="inline-flex items-center justify-center rounded bg-meta-12 py-3 px-10 text-center font-medium text-white hover:bg-opacity-90 dark:bg-meta-3 lg:px-8 xl:px-7"
                    type="submit"
                  >
                    Upload to History
                  </button>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default Translate;
