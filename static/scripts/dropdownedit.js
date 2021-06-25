// var select = document.getElementById("choose");

//variable
var LabelName;
var PlaceholderName;
var LabelInnerhtml;
var InputType = 'text';

var code;

function normalInput(LabelName,LabelInnerhtml,PlaceholderName){
    code = `<div class="field" style='margin-bottom:10px;'>
    <label for="${LabelName}" class="label">${LabelInnerhtml}</label>
    <div class="control">
        <input class="input" type="${InputType}"  name="${LabelName}"  placeholder="${PlaceholderName}">
    </div>
</div>`
}


function doSomething() {
  var select = document.getElementById("choose");
  LabelName = "name";
  LabelInnerhtml = "Name";
  PlaceholderName = "name...";

  // alert(select.value)

  if (select.value == "name") {


    LabelName = "name";
    LabelInnerhtml = "Name";
    PlaceholderName = "name...";
    InputType = 'text'

    normalInput(LabelName,LabelInnerhtml,PlaceholderName)

  }
  else if (select.value == "email") {


    LabelName = "email";
    LabelInnerhtml = "Email";
    PlaceholderName = "email...";
    InputType = 'text'

    normalInput(LabelName,LabelInnerhtml,PlaceholderName)

  }
  else if (select.value == "age") {


    LabelName = "age";
    LabelInnerhtml = "Age";
    PlaceholderName = "age...";
    InputType = 'number'

    normalInput(LabelName,LabelInnerhtml,PlaceholderName)

  }
  else if (select.value == "occ") {


    LabelName = "occ";
    LabelInnerhtml = "Occupation";
    PlaceholderName = "occupation...";
    InputType = 'text'

    normalInput(LabelName,LabelInnerhtml,PlaceholderName)
  }
  else if (select.value == 'status'){
    LabelName = "status";
    LabelInnerhtml = "Status";
    PlaceholderName = "status...";
    InputType = 'text'

    normalInput(LabelName,LabelInnerhtml,PlaceholderName)
  }
  else if (select.value == 'race'){
    LabelName = "race";
    LabelInnerhtml = "Race";
    PlaceholderName = "race...";
    InputType = 'text'

    normalInput(LabelName,LabelInnerhtml,PlaceholderName)
  }
  else if (select.value == 'gender'){
      LabelName = "gender"
      LabelInnerhtml = "Gender"
      PlaceholderName = "gender..."
      code = `
      <label for="${LabelName}" class="label">${LabelInnerhtml}</label>
      <div class="select" style='margin-bottom:10px'>
          <select name="gender" id="gender">
              <option value="Cannot Specify">Cannot Specify</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
          </select>
      </div>`;

  }

  else if (select.value == 'category'){
    LabelName = "category"
    LabelInnerhtml = "Category"
    PlaceholderName = "category..."

    code = ` <label for="${LabelName}" class="label">${LabelInnerhtml}</label>
    <div style="display: flex; margin-bottom:10px">
    <div class="select">
        <select name="category" id="category">
            <option value="Family">Family</option>
            <option value="Friend">Friend</option>
            <option value="Connections">Connections</option>
        </select>
    </div>
    <input  name='others' type="text" style="margin-left: 10px;" class="input" placeholder="others...">
    </div>`
  }

  else if(select.value == 'profile-pic'){
    LabelName = "pic"
    LabelInnerhtml = "Profile Picture"
    PlaceholderName = "image..."
    code = `
    <label for="pic" class="label">Image</label>
    <input style="width: 250px;" class="button" type="file" id="avatar" name="file" accept="image/png  image/jpeg">
      
    
   <br><br>
    ` 
  }
  else{
      code = '<h3 style=" color:red; margin-bottom:5px">*Please select an option to update changes</h3>'
  }

    document.getElementById("mainForm").innerHTML = code;
}
