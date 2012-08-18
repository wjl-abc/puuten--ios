//
//  FriendsViewController.h
//  puuten
//
//  Created by wang jialei on 12-8-14.
//
//

#import <UIKit/UIKit.h>

@interface FriendsViewController : UITableViewController<UITableViewDelegate, UITableViewDataSource>
@property (strong, nonatomic) NSMutableArray *arrayData;

@end
