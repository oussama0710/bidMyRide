function binarySearch(sort, search){
    if (sort[Math.floor(sort.length/2)]>search){
        for (var i=0; i<Math.floor(sort.length/2);i++){
            if (sort[i]===search){
                return true
            }
        }
        return false
    }
    else{
        for (var i=Math.floor(sort.length/2); i<sort.length;i++){
            if (sort[i]===search){
                return true
            }
        }
        return false
    }
}

var nums1 = [1,3,5,6]
var search1= 6
console.log(binarySearch(nums1,search1));