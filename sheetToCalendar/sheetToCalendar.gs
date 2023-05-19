/* 
	Google Spreadsheet To Google Calendar Auto Upload Apps Script
    제 목 :    구글 스프레드시트 -> 구글 캘린더 자동 업로드
    작성일 :    2023.05.20
    세부 기능 :  캘린더 제목 - (타입)내용_담당자
               캘린더 시간 - 시작일 기준 all day 처리
               캘린더 설명 - 시작일~마지막일
			     No.숫자
							 made by PKD
*/

function SynchronizationCal() {

    const sheetTabName = "시트 탭 이름"; // 시트 탭 이름
    const startRow = 11; // 시작 행 번호

    // 대상 시트, 캘린더 저장
    const targetSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetTabName);
    const calendarID = "시트 ID";
    const targetCalendar = CalendarApp.getCalendarById(calendarID);

    // 시트 대상 데이터 집합 생성
    var numRows = targetSheet.getLastRow() - 1; // 시트 전체 행 개수
    var dataRange = targetSheet.getRange(startRow, 1, numRows, targetSheet.getLastColumn());
    var data = dataRange.getValues();

    // Logger.log(data)

    for (i in data) {
        var row = data[i];
        // 상태
        var state = row[1];
        // key 값
        var keyId = "No." + row[2];
        // 일정 제목
        var title = '(' + row[3] + ')' + row[4] + '_' + row[5];
        // 일정 기간 : 오픈일 기준 All day
        var period = new Date(row[6]);
        // 완료 처리 용도 셀 변수
        var stateCol = "B" + (row[2] + 10);
        var cell = targetSheet.getRange(stateCol);

        // 내용 유효성 검사
        if (row[4] == ''){
          continue;
        }

        // 오픈일 유효성 검사
        if (!(period instanceof Date && !isNaN(period))){
          continue;
        }

        // 설명 처리: 기간 표기 (ex. MM.dd~MM.dd) 
        if(!(row[8] == '')){
          var desc = Utilities.formatDate(row[6], "GMT+09:00", "MM.dd") + "~" + Utilities.formatDate(row[8], "GMT+09:00", "MM.dd") + "\n" + keyId;
        } else {
          var desc = Utilities.formatDate(row[6], "GMT+09:00", "MM.dd") + "~ \n" + keyId;
        }

        // Logger.log(title + period + desc);

        var events = targetCalendar.getEventsForDay(period, { search: keyId });

        switch (state){
          case "완료":
            continue;
          
          case "요청":
            // 해당 key 값의 데이터 없을 때에만 일정 추가
            if (events.length == 0){
              targetCalendar.createAllDayEvent(title, period, { description: desc })
            }
            cell.setValue("완료"); // 해당 레코드 완료 처리
            break;
            
          case "수정":
            // 수정할 데이터 없으면, 그냥 일정 추가
            if (events.length == 0) {
              targetCalendar.createAllDayEvent(title, period, { description: desc })
              cell.setValue("완료");
            }
            // 수정할 데이터 1개 있으면, 수정
            else if (events.length == 1) {
              events[0].setTitle(title);
              events[0].setDescription(desc);
              events[0].setAllDayDate(period);
              cell.setValue("완료");
            }
            else {
              continue;
            }
              break;
          default:
            break;
        }
    }
}

function AddCalSyncMenu() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu("Sheet To Calendar").addItem("★업로드 하기★", "SynchronizationCal").addToUi();
}
