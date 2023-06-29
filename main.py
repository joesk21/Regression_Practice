import time
import traceback
import unittest
import os
import platform
from logging import getLogger
from timeit import default_timer
from gappium.webdriver.common.mobileby import MobileBy as By

from lw_helper import LWHelper, LWDriver
from runner.util import info_getter
from runner.util.checklist import load_checkpoints, checkpoint, make_checkpoint, TEST, PASS, FAIL, BLOCK, SKIP
from runner.util.uploader import take_log, start_recordscreen, stop_recordscreen, dump_screen

TESTNAME = "LWQA-24087 선택 상자 크래시"

class RegressionTest(unittest.TestCase):
    def __init__(self, method_name):
        unittest.TestCase.__init__(self, method_name)

        self.logger = getLogger(__name__)
        self.logger.info(f"{self.__class__.__name__}.__init__()")
        #슬래시로 구분하여, 슬래시가 사용되지 않아야 함 PROGRESS(진행), TEST(검증)=Pass, Fail, Block, Skip 기록 가능, sshot=True > 스크린샷을 남김
        #첫 번째 인자 - 영역, 두 번째 - 항목, 세 번째 - 로그 페이지의 스샷 항목
        self._checklist = []
        self._checklist.extend([
            make_checkpoint(TESTNAME, "선택 상자 크래시", "선택 상자 반복 오픈", type=TEST, sshot=True),
            make_checkpoint(TESTNAME, "선택 상자 크래시", "", type=TEST, sshot=True),
            make_checkpoint(TESTNAME, "선택 상자 크래시", "", type=TEST, sshot=True),
            make_checkpoint(TESTNAME, "선택 상자 크래시", "", type=TEST, sshot=True),
            make_checkpoint(TESTNAME, "선택 상자 크래시", "", type=TEST, sshot=True),
            make_checkpoint(TESTNAME, "선택 상자 크래시", "", type=TEST, sshot=True)
        ])

    def collectChecklist(self):
        load_checkpoints(self._checklist, __name__)

        # 반드시 test_로 시작되어야 하며, 테스트 워크벤치 - 테스트 케이스의 이름이 됨
        def test_Regression_104(self):
            test_start = default_timer()
            step = ""
            driver = None
            no_dump = None

            try:
                확인버튼 = "UMG/button_SizeBox/Button/Overlay_0/ScaleBox_0@packedtext=확인"
                보상선택_체크박스_항목="UMG/SizeBox_0/CanvasPanel_1/Img_CheckBox_Press"

                def 보상선택_첫번째항목_클릭(self):
                    """
                    보상 선택 항목에서 첫번째 항목의 체크박스 클릭
                    """
                    self.logger.debug(f"보상선택_첫번째항목_클릭")
                    # 동일한 path 중 0번 인덱스 클릭
                    self.driver.find_elements_by_gameobject_name(보상선택_체크박스_항목)[0].click(0, 1)

                def 확인버튼_클릭(self, UI_이름: str):
                    """
                    보상 선택 UI에서 확인 버튼 클릭
                    """
                    self.logger.debug(f"{UI_이름}_확인버튼_클릭")
                    #
                    btn_Click=self.driver.find_element_by_gameobject_name(확인버튼).click(0,1)
                    btn_Click()
                    if btn_Click:
                        self.logger.debug(f"{UI_이름}_버튼 클릭 성공")
                    else:
                        self.logger.debug(f"{UI_이름}_버튼 클릭 실패")

                def 럭키백_오픈_확인()

                gappium_address = info_getter.get_gappium_address()
                caps = info_getter.get_gappium_caps()

                test_data = info_getter.get_test_data()
                test_env = test_data.get("env", "qa").lower()
                no_dump = test_data.get("no_dump", False)

                account = test_data.get("account")
                password = test_data.get("password")
                server = test_data.get("name")
                character_name = test_data.get("character")

                caps["useGamedroidScreenshot"] = False
                caps["waitTimeForGameUp"] = 30000
                caps["noReset"] = True
                caps["newCommandTimeout"] = 120
                caps["gamedroidTimeout"] = 30000
                caps["overrideExistingSession"] = True

                # Android
                caps["androidInstallTimeout"] = 1000 * 60 * 15
                caps["autoGrantPermissions"] = True
                caps["dontStopAppOnReset"] = False
                caps["appPackage"] = test_data["packageName"]
                caps["appActivity"] = test_data["appActivity"]

                # iOS
                caps["appPushTimeout"] = 300000
                caps["bundleId"] = test_data.get("bundleId", "")

                # Windows (Purple)
                if caps["platformName"].lower() == "windows":
                    caps["automationName"] = "gamewin"

                del caps["app"]

                self.logger.info(f"다음 설정으로 세션을 생성/연결합니다. caps: {caps}")
                try:
                    driver = LWDriver(gappium_address, caps, test_data=test_data)
                except Exception:
                    if caps["platformName"].lower() == "windows":
                        raise Exception("Gappium 세션 연결 중 에러가 발생했습니다: windows")
                    else:
                        self.logger.info("Gappium 세션 연결 중 에러가 발생했기 때문에, 이후 테스트를 수행하지 않도록 프로세스를 종료합니다.")
                        self.logger.error(traceback.format_exc())
                        # if platform.system().lower() == "windows":
                        #     os.system(f"taskkill /F /PID {os.getpid()}")
                        # else:
                        os.system(f"kill {os.getpid()}")

                start_recordscreen(driver, f"{server}_{TESTNAME}", 1800)
                driver.init_gamedroid()
                helper = LWHelper(driver, test_env, country="kr")
                checkpoint(driver, self._checklist, step, PASS)

                step = "/".join(["테스트 준비", "PLAYNC 계정 로그인"])
                self.logger.info(step.rsplit('/', maxsplit=1)[-1])
                check_ingame = helper.로그인.인게임월드_확인()
                if not check_ingame:
                    helper.로그인.로그인_기존캐릭터('PLAYNC', account, password, name, character_name, False)
                    if helper.로그인.인게임월드_확인() and character_name in helper.HUD.캐릭터이름_모두_읽기():
                        self.logger.info("Pass - 월드 입장 성공")

                        if helper.퀴즈.깜짝퀴즈_확인():
                            helper.퀴즈.깜짝퀴즈_풀기()

                        self.logger.info("빌더명령어로 깜작퀴즈를 비활성화합니다.")
                        helper.퀴즈.깜짝퀴즈_비활성화()
                    else:
                        self.logger.info("Fail - 월드 입장 확인에 실패했습니다.")
                        raise Exception("월드 입장 실패")



                step = "/".join([TESTNAME, "선택 상자 크래시", "선택 상자 반복 오픈"])
                helper.공통.빌더명령어_실행("/lw removeallitems", False)
                helper.캐릭터.가방.가방_열기()
                for 시도횟수 in range(4):
                    try:
                        helper.공통.빌더명령어_실행("/lw createitem 903930 1")
                        helper.캐릭터.가방.아이템_사용("스미스의 영웅 각인 방어구 선택 상자")
                        보상선택_첫번째항목_클릭()
                        확인버튼_클릭(self, "보상선택UI")
                        확인버튼_클릭(self, "아이템 획득")
                        self.logger.debug(f"{시도횟수}번째 시도 성공")
                    except:
                        self.logger.debug(f"{시도횟수}번째 시도 실패")







            except Exception:
                # 테스트를 더이상 진행할 수 없는 경우 Block 처리
                self.logger.error(traceback.format_exc())
                checkpoint(driver, self._checklist, step, BLOCK)

                try:
                    if not no_dump:
                        dump_screen(driver)
                except Exception:
                    self.logger.error("dump_screen 실패")
                    self.logger.error(traceback.format_exc())
                take_log(driver)
                stop_recordscreen(driver)

                try:
                    driver.quit()
                except Exception:
                    self.logger.error("driver quit 실패")
                    self.logger.error(traceback.format_exc())

            elapsed_time = default_timer() - test_start
            self.logger.info(f"테스트 수행 시간: {int(elapsed_time / 60)}분 {int(elapsed_time % 60)}초")









