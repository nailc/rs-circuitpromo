/*
 * Copyright (c) 2013, 9279-5749 Qu�bec inc and/or its affiliates. All rights reserved.
 * Etienne Lord, Alix Boc
 * PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.
 */
var PanierCtrl = function (	$scope, $routeParams, $http, $locale, $location, $dialog,$filter, Langue, Produit, User) {
			$scope.phantomJS_panier_ready=false;
			$scope.produit=Produit.data;			
			$scope.current_panier=User.CURRENT_PANIER();//--Important			
			$scope.panier_items=[];
			
		
			$scope.desktopwidth=function() {							
							return ($(window).width()>980);
						}
		
			//--Get a product from the data
			$scope.getProduit = function(id_produit) {				 									
					return Produit.getProduit(id_produit,User.USER_DATABASE(), User.LANGUE(), $http, function(data) {						
							//--Replace the scope item with this new item						
							for (var j=0; j<$scope.panier_items.length;j++) {							
									if ($scope.panier_items[j].i==data.i) {
										$scope.panier_items[j]=data;
										return;
									}								
							}
					});
					console.log($scope.panier_items);
			}
			
			$scope.getItems = function(id_panier) {													
				var items=User.getItems(id_panier);								
				var tmp=[];		
				$scope.panier_items=tmp; //[] for IE				
				//--Only update the list, they will be added in the callback...
				for (var i=0; i<items.length;i++) {
					//console.log(items[i]);
					tmp[i]=$scope.getProduit(items[i].i);
					// Ligne ajoutée temporairement par Nail le 28-02-2021 le temps de trouver une solution a long terme
					if (tmp[i].d==0){
						tmp[i].d=items[i].d;
						}
				}		
				return tmp;


			}
						
			if (isDefine($routeParams.id_panier)) {
				$scope.id_panier=$routeParams.id_panier;				
				$scope.panier_items=$scope.getItems($scope.id_panier);		
				
			} else {
				$scope.id_panier=$scope.current_panier;
				$scope.panier_items=$scope.getItems($scope.id_panier);							
			}			
			
			$scope.$watch('Produit.produit', function() {	
				$scope.panier_items=$scope.getItems($scope.id_panier);			
			});
			
			$scope.$watch('totalquantity()', function() {				
				//--Only update if we add from the search list...				
				if (!$scope.update_panier) {
					$scope.panier_items=$scope.getItems($scope.id_panier);			
				}
			});
			
			$scope.deleteProductPanier =function(data, quantity_to_remove) {															
						
						if (User.removeProduct(data)) {
							$scope.update_panier=true;
							$scope.panier_items=$scope.getItems($scope.id_panier);
							//--$scope.panier=User.getHash();//--MainCtrl							
						}
						
				
			}
			
			$scope.getTitle = function(id_panier) {
				if (id_panier==$scope.current_panier){
					return $scope.langue.l_grocerylist;
				} //Ajouté par Nail 
				else if(id_panier==1111111111111){ 
					return $scope.langue.l_recommended_list+" ("+$scope.totalquantity(id_panier)+" "+$scope.langue.l_produit+")";
				} //Fin ajouté par Nail
				else {
					return $scope.langue.l_archive_sing+" ("+$scope.totalquantity(id_panier)+" "+$scope.langue.l_produit+")";
				}
			}
					
			
			$scope.getCategorie =function(id_categorie) {
				var cat=Produit.getCategorie(id_categorie);
				if ($scope.lg=='fr') {
					return cat.cnf;
				} else {
					return cat.cne;
				}
			}
				
			
			$scope.infocolor = function(totalThisItem, color) {
				if (totalThisItem==0) return "grey";
				if (isDefine(color)) return color;
				return "black";
			}
			
			$scope.totalquantity = function(id_panier) {				 					
				if (!isDefine(id_panier)||$scope.current_panier==id_panier) {
					return User.panier['totalquantity'];
				} else {
					return User.totalquantity(id_panier);
				}					
			}
			
			$scope.total = function(id_panier) {				 
				if (!isDefine(id_panier)||$scope.current_panier==id_panier) {
					return User.panier['total'];
				} else {
					return User.total(id_panier);
				}						
			}
			
			$scope.totalSansSpecial = function(id_panier) {				 
				if (!isDefine(id_panier)||$scope.current_panier==id_panier) {
					return User.panier['totalSansSpecial'];
				} else {
					return User.totalSansSpecial(id_panier);
				}						
			}
						
			$scope.getProduitFromPanier=function(data) {															
					if (!isDefine(Produit.produit)) return "";			
							var result = $.grep(Produit.produit, function(e){ return e.p == data.p; });				
							if (!isDefine(result)) return "";
							return result[0];					
		   }			
			
			$scope.totalCurrentPanier=function(produit,id_panier) {
				if ($scope.inCurrentPanier(produit)) {
					return User.panier[produit.i].quantity;
				} else {				
					return User.totalCurrentPanier(produit,id_panier);
				}
			}
			
			
			
			$scope.setCategoriesNav = function (id_categorie) {			
				$scope.$parent.selected_categories=[id_categorie];		
				$scope.go('/produit');
			}
			
			
			////////////////////////////////////////////////
			/// DELETE List dialog
			
			 $scope.showDeleteDialog = function(panier){
					var title = $scope.langue.l_supprimer_list;
					var msg = $scope.langue.l_supprimer_list2+': '+$filter('datelg','dd MMMM yyyy - hh:mm a')(panier)+' ('+$scope.totalquantity(panier)+' items )';
					var btns = [{result:'cancel', label: $scope.langue.l_cancel}, {result:'ok', label: 'OK', cssClass: 'btn-primary'}];

					$dialog.messageBox(title, msg, btns)
					  .open()
					  .then(function(result){
						if (result=='ok') {
							User.removePanier(panier);
						}
					});
				  };
			
			
			////////////////////////////////////////////////
			//--Show more for this panier
				$scope.pagesShown = 1;
				$scope.pageSize = 4; //--Put a load more button -- Fix IE8	
								
				$scope.itemsLimit = function(limit) {					
					return $scope.pageSize * $scope.pagesShown;
				};
				$scope.hasMoreItemsToShow = function() {										
					return $scope.pagesShown < ($scope.panier_items.length / $scope.pageSize);
				};
				
				$scope.showMoreItems = function() {
					$scope.pagesShown = $scope.pagesShown + 1;         
				};

				// Added by Nail 03/02/2020.
				$scope.selectAll = true;
				$scope.selected = [];


				

				$scope.logPanier = function	(){
					var panArr = [];
					var taffy_tmp = [];
					for (var i = 0; i < $scope.truePaniers().length; i++){
						if ($scope.selected [i] == true){
							panArr.push($scope.truePaniers()[i]);
						}
					}
					var taffy_connected = JSON.parse(localStorage.getItem('taffy_Liste'));
					for (var element in panArr){
						for (var property in taffy_connected){
							if (panArr[element] == taffy_connected[property].c){
								taffy_tmp.push(taffy_connected[property]);
							}
						}
					}
					
					var taffy_tmp_str = JSON.stringify(taffy_tmp);
					console.log(taffy_tmp_str)
					var province = localStorage.getItem('USER_DATABASE');
					var sendData = function(){
						$("#loading_info").show();
						//$("#loadingImage").show();
					    $.post('testAPI.php', 
					    		{taffy_tmp_str: taffy_tmp_str,
					    		 province: province}, function(response){
							new_taffy = JSON.parse(response);
							//console.log(province, response);
							/*old_taffy  = localStorage.getItem('taffy_Liste');
							old_taffy = JSON.parse(old_taffy);
							var value = 1111111111111;
							for(var key in Object.keys(old_taffy)){
								var val = Object.values(old_taffy)[key].c;
							  if(val == value){
							  	//console.log(old_taffy[key]);
							    old_taffy[key] = undefined;
							  }
							}
							Object.keys(old_taffy).forEach(key => old_taffy[key] === undefined && delete old_taffy[key])
							
							var i = 0;
							for(var key in Object.keys(old_taffy)){
								console.log(old_taffy[1]);
						    	old_taffy[i]=old_taffy[key];
						    	old_taffy[key]=undefined;
								i++;
							}
							Object.keys(old_taffy).forEach(key => old_taffy[key] === undefined && delete old_taffy[key])
							console.log(old_taffy);*/


							new_taffy = JSON.parse(new_taffy);
							//t3 = old_taffy.concat(new_taffy);
							//console.log(t3);
							localStorage.setItem('taffy_Liste', JSON.stringify(new_taffy));
							$("#loading_info").hide();
							location.reload();
							window.location = "/#!/panier/1111111111111"

							});
					}
					sendData();
					;
				};
				//Added by Nail to check if user is connected
				$scope.is_connected = localStorage.getItem("USER_CONNECTED");
				console.log($scope.is_connected)


				$scope.current_panier_id = function (){
					return $scope.current_panier;
				};

				$scope.get_paniers_count = function() {
					return $scope.truePaniers().length;
				};

				$scope.togglePanier = function(index) {
	              $scope.truePaniers()[index].checked = !$scope.truePaniers()[index].checked;
	              if (!$scope.truePaniers()[index].checked) {
	                $scope.selectAll = false;
	              }
	            };

	            /*$scope.toggleDefault = function(){
	            	if(window.location.hash == '#!/panier'){
						var checked = $scope.selectAll;
	              		for (var i = 0; i < $scope.truePaniers().length; i++) {
	                		$scope.selected[i] = checked;
	              		}
	            	}
	            };*/

	            $scope.toggleAll = function() {
	              var checked = $scope.selectAll;
	              for (var i = 0; i < $scope.truePaniers().length; i++) {
	                $scope.selected[i] = checked;
	              }
	            };
	            // End added by Nail.

				$scope.totalMore = function() {					
					var t=$scope.panier_items.length-($scope.pagesShown*$scope.pageSize);
					if (t>0) return t;
					return 0;
				};
				
				$scope.listPanier = function() {				 
							return User.listPanier();
				};
				$scope.truePaniers = function () {
					return User.listPanier().filter(function(o) {
						return o != 1111111111111;
					});
				};
				$scope.recommendations = function () {
					return User.listPanier().filter(function(o) {
						return o == 1111111111111;
					});	
				};

				
				 $scope.$on('$viewContentLoaded', function() {							
							//--PhantomJS
							$scope.phantomJS_panier_ready=true;
				});		
			
			////////////////////////////////////////////////
			//--Show more for the list OF Panier
				$scope.pagesPanierShown = 1;
				$scope.pagePanierSize = 10;	
				
				$scope.PanierLimit = function(limit) {									
					return $scope.pagePanierSize * $scope.pagesPanierShown;
				};
				
				$scope.hasMorePanierToShow = function() {										
					return $scope.get_paniers_count() > $scope.PanierLimit();
				};
				
				$scope.showMorePanier = function() {
					$scope.pagesPanierShown = $scope.pagesPanierShown + 1;         
				};
				
				$scope.totalMorePanier = function() {
					var t=$scope.listPanier().length-($scope.pagesPanierShown*$scope.pagePanierSize);
					if (t>0) return t;
					return 0;
				};
			//console.log($scope.panier_items);
		}
